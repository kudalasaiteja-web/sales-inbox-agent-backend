# Design Decisions

## Stack

- **Backend**: Python + FastAPI. Chosen for speed of development, automatic
  interactive docs (`/docs`), and built-in request validation via Pydantic —
  important given the assignment explicitly grades rejection of invalid enum
  values (§5.1).
- **Database**: MongoDB Atlas (cloud-hosted), not local SQLite. Free-tier hosts
  like Render often use ephemeral disk storage that can be wiped on redeploy —
  a real risk for an assignment that's graded by re-running requests against a
  live deployment days after submission. A separate, always-on cloud database
  removes that risk entirely, at the cost of slightly more setup (Atlas account,
  connection string, network access config) than a zero-setup SQLite file.
- **AI**: Google Gemini (`gemini-flash-latest`), via a single structured-JSON
  prompt per email rather than a fine-tuned model or a chain of multiple calls.
  A single well-specified prompt was sufficient to correctly handle every trap
  case in the eval set (see EVALS.md), so added complexity (multi-step chains,
  separate classification + extraction calls) wasn't justified for this scope.
- **Frontend**: React + Vite. Minimal component structure, no external state
  library (plain `useState`/`useEffect` was sufficient for three simple panels:
  ingest, table, chat) and no CSS framework — inline styles were enough for a
  functional, unstyled-but-clear submission.

## Routing engine design

- **Rules encoded as plain-English instructions in the prompt**, not as a
  separate rules engine or decision tree in code. This makes the rules easy to
  read and modify (they live in one place, `routing.py`'s `ROUTING_RULES`
  string) and lets the LLM handle judgment calls — like distinguishing spam
  from genuine marketing outreach — that a rigid rules engine would struggle
  with using keyword matching alone.
- **Explicit rule ordering with override priority** (e.g. "PSU tenders always
  go to Aarti regardless of value" is stated as overriding the general
  value-based rule) rather than leaving precedence implicit. This directly
  addresses the "PSU tender below value threshold" trap case called out in the
  assignment brief.
- **The model is asked to output `null` rather than guess** for fields it can't
  confidently determine (`due_date`, `deal_value_inr`, `company_name`) — this
  was an explicit instruction in the prompt (Rule 9) to reduce hallucinated
  values that would otherwise silently corrupt task data.

## Persistence & idempotency

- **Idempotency check happens before calling Gemini**, not after. If a
  `source_email_id` has already been processed for a candidate, we skip it
  immediately — this both prevents duplicate tasks on re-runs (required for
  grading Run 2, §8.1) and avoids burning API quota re-classifying emails
  we've already handled.
- **Thread replies update the existing task via `PATCH`** rather than creating
  a new one, keyed on matching `thread_id` + the email being marked `is_reply`.
  This was tested explicitly (see conversation/eval history) with a real
  budget-revision reply that correctly updated `deal_value_inr` and `due_date`
  on the original task without creating a duplicate.

## Chat interface

- **`/api/chat` retrieves real stored task data first, then asks Gemini to
  answer using only that data** (a lightweight retrieval-augmented pattern),
  rather than letting the model answer from general knowledge or its own
  memory of the conversation. This was a deliberate choice to avoid
  hallucinated numbers when answering questions like "what's the biggest deal
  value" — the answer must trace back to real database contents.

## Known limitations / things I'd improve with more time

- **Gemini free-tier rate limits** (~20 requests/day per project) meant testing
  and evaluation required careful pacing and, at times, creating a fresh
  project to continue development. A production version would need a
  billing-enabled project from the start.
- **Error handling in `/ingest` is per-email but not retried** — if a single
  email's Gemini call fails after retries are exhausted, it's recorded in the
  `errors` array and skipped, but there's no automatic retry queue for
  transient failures on a later run.
- **No automated test suite** — testing was done manually and via one-off
  scripts (`test_routing.py`, `run_eval.py`) rather than a proper `pytest`
  suite with CI. Given more time, I'd convert these into a real test suite
  that runs on every push.
- **Frontend has no loading skeletons or error boundaries** — errors currently
  surface as plain text; a production version would need friendlier error
  states and loading indicators throughout.

## One thing my system gets wrong that I knowingly shipped anyway

The `/api/chat` endpoint re-hits Gemini on every single question, even for simple
aggregate questions like "how many tasks does Aarti have" that are fully answerable
by a direct database query alone. This means:
- Every chat question costs an API call and adds 1-3 seconds of latency, even for
  trivial lookups.
- Under the free-tier's ~20 requests/day cap, a handful of chat questions can
  meaningfully eat into the same quota budget as email classification.

The correct fix would be to detect simple aggregate/lookup questions (counts, sums,
filters) and answer them directly from `/api/stats`-style queries without touching
Gemini at all — reserving the LLM call only for questions that genuinely need
natural-language reasoning over the task data (e.g. "which of these look most
urgent and why"). I chose not to build that routing layer given time constraints,
since the current approach is still correct (grounded in real stored data, never
hallucinated) — just not as cheap or fast as it could be.

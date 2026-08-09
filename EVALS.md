# Evaluation Report

## Method

A hand-labeled set of 12 test emails was constructed, covering both straightforward
cases and known "trap" cases explicitly called out in the assignment brief:
tender/PSU value-threshold overrides, marketing sponsorships with monetary amounts,
vendor spam disguised as marketing language, out-of-office auto-replies, newsletters,
and a genuinely ambiguous multi-intent email.

Each email was run through the live routing engine (`classify_email()` in `routing.py`,
backed by Gemini `gemini-flash-latest`), and the output was compared against a
hand-labeled expected answer for `should_create_task`, `assignee_id`, and `category`.

Run with: `python run_eval.py` (see `eval_set.py` for the full labeled dataset).

## Results

**Accuracy: 12/12 correct (100%)**

| # | Case | Expected | Got | Result |
|---|------|----------|-----|--------|
| 0 | Enterprise RFP (Meridian Steel) | u_aarti / enterprise_rfp | u_aarti / enterprise_rfp | ✅ |
| 1 | SMB demo request | u_rohit / smb_enquiry | u_rohit / smb_enquiry | ✅ |
| 2 | PSU tender below ₹10L threshold | u_aarti / enterprise_rfp | u_aarti / enterprise_rfp | ✅ |
| 3 | Marketing sponsorship with money | u_meera / marketing | u_meera / marketing | ✅ |
| 4 | Finance invoice | u_divya / finance | u_divya / finance | ✅ |
| 5 | Out-of-office auto-reply | no task | no task | ✅ |
| 6 | Vendor spam (marketing-flavored) | no task | no task | ✅ |
| 7 | Reseller/alliance proposal | u_karan / alliances | u_karan / alliances | ✅ |
| 8 | Newsletter | no task | no task | ✅ |
| 9 | Ambiguous multi-intent email | u_triage | u_triage | ✅ |
| 10 | Government e-tender | u_aarti / enterprise_rfp | u_aarti / enterprise_rfp | ✅ |
| 11 | Enterprise pricing enquiry | u_aarti / enterprise_rfp | u_aarti / enterprise_rfp | ✅ |

## Analysis

The system correctly handled every trap case in this eval set, including the two
hardest ones called out in the assignment brief:

- **Case 2 (PSU tender)**: correctly overrode the ₹10L value-based routing rule
  because the sender was a government/PSU entity, matching Rule 2's priority
  over Rule 3.
- **Case 6 (vendor spam)**: correctly distinguished *direction of intent* — the
  email used marketing-sounding language (content, PR, webinar) but was someone
  selling services *to* us, not a genuine inbound sponsorship/collaboration ask.
  This is the single failure mode the assignment brief flags as most common
  among naive keyword-matching approaches.

## Known limitations

- **Sample size**: 12 hand-labeled cases is a small eval set. It covers each rule
  and trap case at least once, but a production system would need a much larger
  labeled set (50+) for statistically meaningful precision/recall numbers,
  especially to catch rarer edge cases not represented here.
- **Gemini free-tier rate limits**: the free tier caps requests at roughly 20/day
  per project. During evaluation, several calls hit this limit and required
  automatic retries with backoff (see `run_eval.py`). For processing the full
  250-email dataset, this would need either a billing-enabled Gemini project
  (Flash pricing is a few cents per 1,000 requests) or batching across multiple
  days/API keys.
- **No adversarial cases tested yet**: this eval set does not include emails
  deliberately designed to confuse the model further (e.g. mixed-language emails,
  emails with conflicting signals in subject vs. body, or very long emails with
  the actual ask buried in the middle). These would be good additions to a v2
  eval set.
- **Single model run per case**: each email was classified once. Given LLM output
  can vary slightly between runs, a more rigorous eval would run each case
  multiple times and check for consistency, not just a single correct answer.
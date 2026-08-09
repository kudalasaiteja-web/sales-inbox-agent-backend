import json
import time
import random
import os
from routing import classify_email

random.seed(7)

BATCH_LIMIT = 15  # safely under the free-tier daily cap

with open("inbox_250.json", "r", encoding="utf-8") as f:
    all_emails = json.load(f)

with open("eval_answer_key.json", "r", encoding="utf-8") as f:
    answer_key = json.load(f)

# Pick the same 50 emails every time (fixed seed = reproducible sample)
sample = random.sample(all_emails, 50)

# Load existing progress if we have any
RESULTS_FILE = "eval_results_50.json"
if os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        results = json.load(f)
else:
    results = []

already_done_ids = {r["email_id"] for r in results}
remaining = [e for e in sample if e["email_id"] not in already_done_ids]

print(f"Already processed: {len(already_done_ids)}/50")
print(f"Remaining: {len(remaining)}")

if not remaining:
    print("All 50 already processed! Skipping straight to scoring below.")
else:
    todo = remaining[:BATCH_LIMIT]
    print(f"Processing {len(todo)} more emails this run...\n")

    for i, email in enumerate(todo):
        email_id = email["email_id"]
        expected = answer_key[email_id]

        print(f"Processing {i+1}/{len(todo)} ({email_id})...")

        try:
            got = classify_email(email)
            results.append({"email_id": email_id, "expected": expected, "got": got, "error": False})
        except Exception as e:
            print(f"  Failed: {e}")
            results.append({"email_id": email_id, "expected": expected, "got": None, "error": True})

        # Save progress after EVERY email, so a crash never loses work
        with open(RESULTS_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        time.sleep(4)

    print(f"\nBatch done. Total processed so far: {len(results)}/50")
    if len(results) < 50:
        print("Run this script again (tomorrow, or once quota resets) to continue.")

# ---------- Scoring (only runs meaningfully once all 50 are done, but safe to run anytime) ----------

if len(results) < 50:
    print(f"\nNot all 50 done yet ({len(results)}/50) — skipping final scoring for now.")
else:
    categories = ["enterprise_rfp", "smb_enquiry", "marketing", "alliances", "finance", "triage"]
    stats = {c: {"tp": 0, "fp": 0, "fn": 0} for c in categories}

    correct_count = 0
    spurious = []
    missed = []
    misrouted = []

    for r in results:
        if r["error"]:
            continue
        expected = r["expected"]
        got = r["got"]

        exp_create = expected.get("should_create_task")
        got_create = got.get("should_create_task")

        if not exp_create and not got_create:
            correct_count += 1
            continue

        if not exp_create and got_create:
            spurious.append(r)
            cat = got.get("category")
            if cat in stats:
                stats[cat]["fp"] += 1
            continue

        if exp_create and not got_create:
            missed.append(r)
            cat = expected.get("category")
            if cat in stats:
                stats[cat]["fn"] += 1
            continue

        exp_cat = expected.get("category")
        got_cat = got.get("category")
        exp_assignee = expected.get("assignee_id")
        got_assignee = got.get("assignee_id")

        if exp_cat == got_cat and exp_assignee == got_assignee:
            correct_count += 1
            if exp_cat in stats:
                stats[exp_cat]["tp"] += 1
        else:
            misrouted.append(r)
            if got_cat in stats:
                stats[got_cat]["fp"] += 1
            if exp_cat in stats:
                stats[exp_cat]["fn"] += 1

    total_scored = len([r for r in results if not r["error"]])
    print(f"\n=== OVERALL ===")
    print(f"Scored: {total_scored}/50 (errors excluded: {50 - total_scored})")
    print(f"Correct: {correct_count}/{total_scored} = {correct_count/total_scored*100:.1f}%")
    print(f"Spurious: {len(spurious)}  Missed: {len(missed)}  Misrouted: {len(misrouted)}")

    print(f"\n=== PER-CATEGORY PRECISION / RECALL ===")
    for c in categories:
        tp, fp, fn = stats[c]["tp"], stats[c]["fp"], stats[c]["fn"]
        precision = tp / (tp + fp) if (tp + fp) > 0 else None
        recall = tp / (tp + fn) if (tp + fn) > 0 else None
        p_str = f"{precision*100:.0f}%" if precision is not None else "N/A"
        r_str = f"{recall*100:.0f}%" if recall is not None else "N/A"
        print(f"  {c}: precision={p_str}, recall={r_str} (tp={tp}, fp={fp}, fn={fn})")

    if spurious:
        print(f"\n=== SPURIOUS ===")
        for r in spurious:
            print(f"  {r['email_id']}: expected skip, got {r['got'].get('category')}/{r['got'].get('assignee_id')}")
    if missed:
        print(f"\n=== MISSED ===")
        for r in missed:
            print(f"  {r['email_id']}: expected task, got skip")
    if misrouted:
        print(f"\n=== MISROUTED ===")
        for r in misrouted:
            print(f"  {r['email_id']}: expected {r['expected'].get('assignee_id')}/{r['expected'].get('category')}, "
                  f"got {r['got'].get('assignee_id')}/{r['got'].get('category')}")
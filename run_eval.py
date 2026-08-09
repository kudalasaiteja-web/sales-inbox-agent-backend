import time
from eval_set import EVAL_CASES
from routing import classify_email

correct = 0
total = len(EVAL_CASES)
mistakes = []

for i, case in enumerate(EVAL_CASES):
    print(f"Processing {i+1}/{total}...")

    # Retry up to 3 times if we hit a rate limit
    for attempt in range(3):
        try:
            result = classify_email(case["email"])
            break
        except Exception as e:
            print(f"  Rate limited, waiting 30s... (attempt {attempt+1})")
            time.sleep(30)
    else:
        print(f"  Skipping email {i} after 3 failed attempts")
        continue

    expected = case["expected"]

    is_correct = True
    for key, expected_value in expected.items():
        if result.get(key) != expected_value:
            is_correct = False

    if is_correct:
        correct += 1
    else:
        mistakes.append({
            "index": i,
            "subject": case["email"]["subject"],
            "expected": expected,
            "got": {k: result.get(k) for k in expected.keys()}
        })

    time.sleep(4)  # small pause between calls to avoid rate limits

print(f"\nAccuracy: {correct}/{total} = {correct/total*100:.1f}%\n")

if mistakes:
    print("Mistakes:")
    for m in mistakes:
        print(f"\n  Email #{m['index']}: {m['subject']}")
        print(f"    Expected: {m['expected']}")
        print(f"    Got:      {m['got']}")
else:
    print("No mistakes! All cases passed.")
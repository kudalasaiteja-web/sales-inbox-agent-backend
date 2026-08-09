from routing import classify_email

test_cases = {
    "Example 3 - PSU tender below threshold (should still go to Aarti)": {
        "from_name": "BHEL Procurement",
        "from_email": "procurement@bhel.in",
        "subject": "Tender Notice No. BHEL/PROC/2026/0847",
        "body": "Bharat Heavy Electricals Limited invites bids for supply of analytics software licences. Estimated value: Rs. 6,50,000. Last date for bid submission: 03-08-2026, 1700 hrs IST.",
        "received_at": "2026-08-01T14:20:00+05:30",
        "is_reply": False
    },
    "Example 7 - Out of office (should create NO task)": {
        "from_name": "Suresh Kulkarni",
        "from_email": "s.kulkarni@meridiansteel.co.in",
        "subject": "Out of Office",
        "body": "I am out of office until 14th August with limited access to email. For urgent matters please contact my colleague at raghav@northbridge.in. — Sent from Outlook",
        "received_at": "2026-08-03T08:00:00+05:30",
        "is_reply": True
    },
    "Example 8 - Vendor spam disguised as marketing (should create NO task)": {
        "from_name": "GrowthHackers SEO",
        "from_email": "outreach@growthhackers.biz",
        "subject": "Free audit - boost your organic traffic",
        "body": "Hi, I noticed your website isn't ranking on page 1 for key terms. We've helped 200+ SaaS companies 3x their organic traffic. We do content marketing, PR outreach, and webinar promotion. Free audit attached — interested in a quick 15 min call?",
        "received_at": "2026-08-02T10:00:00+05:30",
        "is_reply": False
    },
    "Example 4 - Marketing sponsorship with money (should go to Meera, NOT sales)": {
        "from_name": "Nandita Reddy",
        "from_email": "nandita@saassummit.in",
        "subject": "Sponsorship confirmation needed",
        "body": "We're finalising sponsors for the India SaaS Summit in Bengaluru. Gold tier is ₹4,00,000 and includes a keynote slot. We need confirmation by tomorrow EOD as we're going to print. — Nandita Reddy, Sponsorship Lead",
        "received_at": "2026-08-02T16:45:00+05:30",
        "is_reply": False
    }
}

for label, email in test_cases.items():
    print(f"\n=== {label} ===")
    result = classify_email(email)
    print(result)
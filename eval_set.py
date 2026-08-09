EVAL_CASES = [
    {
        "email": {
            "from_name": "Suresh Kulkarni", "from_email": "s.kulkarni@meridiansteel.co.in",
            "subject": "RFP - Enterprise DMS", "is_reply": False,
            "received_at": "2026-08-01T09:14:22+05:30",
            "body": "Meridian Steel invites proposals for an enterprise DMS. Indicative budget is Rs. 25 lakhs. Proposals must reach us by 12th August 2026."
        },
        "expected": {"should_create_task": True, "assignee_id": "u_aarti", "category": "enterprise_rfp"}
    },
    {
        "email": {
            "from_name": "Ankit Bose", "from_email": "ankit@railyardlogistics.in",
            "subject": "Quick demo request", "is_reply": False,
            "received_at": "2026-08-01T11:02:00+05:30",
            "body": "Hi, we're a 30-person logistics startup. Can we get a demo sometime next week? Nothing urgent."
        },
        "expected": {"should_create_task": True, "assignee_id": "u_rohit", "category": "smb_enquiry"}
    },
    {
        "email": {
            "from_name": "BHEL Procurement", "from_email": "procurement@bhel.in",
            "subject": "Tender Notice BHEL/PROC/2026/0847", "is_reply": False,
            "received_at": "2026-08-01T14:20:00+05:30",
            "body": "BHEL invites bids for analytics software licences. Estimated value: Rs. 6,50,000. Last date: 03-08-2026."
        },
        "expected": {"should_create_task": True, "assignee_id": "u_aarti", "category": "enterprise_rfp"}
    },
    {
        "email": {
            "from_name": "Nandita Reddy", "from_email": "nandita@saassummit.in",
            "subject": "Sponsorship confirmation needed", "is_reply": False,
            "received_at": "2026-08-02T16:45:00+05:30",
            "body": "Gold tier sponsorship is ₹4,00,000 and includes a keynote slot. Need confirmation by tomorrow EOD."
        },
        "expected": {"should_create_task": True, "assignee_id": "u_meera", "category": "marketing"}
    },
    {
        "email": {
            "from_name": "Vantage Cloud Billing", "from_email": "billing@vantagecloud.co.in",
            "subject": "Invoice INV-2026-0331 overdue", "is_reply": False,
            "received_at": "2026-08-02T10:00:00+05:30",
            "body": "Invoice INV-2026-0331 for Rs. 1,18,000 against PO-88214 is 12 days overdue."
        },
        "expected": {"should_create_task": True, "assignee_id": "u_divya", "category": "finance"}
    },
    {
        "email": {
            "from_name": "Suresh Kulkarni", "from_email": "s.kulkarni@meridiansteel.co.in",
            "subject": "Out of Office", "is_reply": True,
            "received_at": "2026-08-03T08:00:00+05:30",
            "body": "I am out of office until 14th August. For urgent matters contact raghav@northbridge.in."
        },
        "expected": {"should_create_task": False}
    },
    {
        "email": {
            "from_name": "GrowthHackers SEO", "from_email": "outreach@growthhackers.biz",
            "subject": "Free audit - boost your organic traffic", "is_reply": False,
            "received_at": "2026-08-02T10:00:00+05:30",
            "body": "We do content marketing, PR outreach, and webinar promotion. Free audit attached - interested in a call?"
        },
        "expected": {"should_create_task": False}
    },
    {
        "email": {
            "from_name": "TechPartners Reseller", "from_email": "biz@techpartners.io",
            "subject": "Reseller partnership proposal", "is_reply": False,
            "received_at": "2026-08-03T12:00:00+05:30",
            "body": "We'd like to become a reseller for your product in the APAC region. We already work with 50+ clients generating $2M annually."
        },
        "expected": {"should_create_task": True, "assignee_id": "u_karan", "category": "alliances"}
    },
    {
        "email": {
            "from_name": "Newsletter Weekly", "from_email": "noreply@techdigest.com",
            "subject": "This week in SaaS: 10 trends to watch", "is_reply": False,
            "received_at": "2026-08-04T07:00:00+05:30",
            "body": "Here's your weekly roundup of SaaS industry news and trends. Unsubscribe anytime."
        },
        "expected": {"should_create_task": False}
    },
    {
        "email": {
            "from_name": "Priya Nair", "from_email": "priya@confused-corp.com",
            "subject": "Question", "is_reply": False,
            "received_at": "2026-08-04T15:00:00+05:30",
            "body": "Hi, not sure who to ask, but we might be interested in either a demo or possibly reselling your product, or maybe sponsoring your next event. Can someone call me?"
        },
        "expected": {"should_create_task": True, "assignee_id": "u_triage"}
    },
    {
        "email": {
            "from_name": "State Govt Procurement", "from_email": "tenders@maharashtra.gov.in",
            "subject": "e-Tender for Software Services", "is_reply": False,
            "received_at": "2026-08-05T09:00:00+05:30",
            "body": "Government of Maharashtra invites e-tenders for software services. Estimated value Rs 3,00,000. Submission deadline: 06-08-2026."
        },
        "expected": {"should_create_task": True, "assignee_id": "u_aarti", "category": "enterprise_rfp"}
    },
    {
        "email": {
            "from_name": "Rahul Verma", "from_email": "rahul@midsizeco.in",
            "subject": "Enterprise plan pricing", "is_reply": False,
            "received_at": "2026-08-05T13:00:00+05:30",
            "body": "We're a 500-person company evaluating your enterprise plan. Budget is around Rs. 15,00,000. Could we schedule a call this week?"
        },
        "expected": {"should_create_task": True, "assignee_id": "u_aarti", "category": "enterprise_rfp"}
    }
]
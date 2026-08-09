import json
import random
from datetime import datetime, timedelta

random.seed(42)  # reproducible output

# ---------- Building blocks ----------

ENTERPRISE_COMPANIES = ["Meridian Steel", "Vantage Industries", "Bharat Textiles", "Continental Auto Parts",
                          "Skyline Constructions", "Orion Pharmaceuticals", "Deccan Logistics Group", "Aravalli Cements"]
SMB_COMPANIES = ["Railyard Logistics", "BrightPath Consulting", "Nimbus Analytics", "GreenLeaf Foods",
                  "PixelForge Studio", "QuickCart Retail", "Sunrise Bakery Co", "Vertex Fitness"]
PSU_ENTITIES = ["Bharat Heavy Electricals Limited", "Indian Oil Corporation", "Steel Authority of India",
                 "Coal India Limited", "Government of Maharashtra", "Government of Karnataka", "NTPC Limited"]
EVENT_NAMES = ["India SaaS Summit", "TechCon Bengaluru", "Startup Mahakumbh", "CloudNext Conference",
                "B2B Growth Summit", "FinTech Forward Expo"]
RESELLER_COMPANIES = ["TechPartners Reseller", "Alliance Systems Integrators", "NorthBridge Channel Partners",
                        "Digital Gateway Solutions", "Prime Integration Services"]
VENDOR_COMPANIES = ["Vantage Cloud", "DataStream Billing", "CoreServe Utilities", "Apex Software Licensing",
                     "GlobalPay Systems"]
SPAM_COMPANIES = ["GrowthHackers SEO", "LeadGen Pro", "ClickBoost Marketing", "RankFirst Agency", "TrafficMax Digital"]
NEWSLETTER_SOURCES = ["TechDigest Weekly", "SaaS Insider", "The Sales Brief", "Founder's Weekly"]

FIRST_NAMES = ["Suresh", "Ankit", "Priya", "Rahul", "Nandita", "Karthik", "Meena", "Vikram", "Divya", "Arjun", "Kavya", "Rohan"]
LAST_NAMES = ["Kulkarni", "Bose", "Nair", "Verma", "Reddy", "Iyer", "Singh", "Patel", "Menon", "Rao"]

def random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def random_email(name, domain):
    first = name.split()[0].lower()
    return f"{first}@{domain}"

def random_date(start="2026-07-15", end="2026-08-09"):
    start_d = datetime.fromisoformat(start)
    end_d = datetime.fromisoformat(end)
    delta = (end_d - start_d).days
    d = start_d + timedelta(days=random.randint(0, delta), hours=random.randint(8, 18), minutes=random.randint(0, 59))
    return d

def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S+05:30")

def deadline_str(received_dt, hours_ahead):
    dl = received_dt + timedelta(hours=hours_ahead)
    return dl.strftime("%d-%m-%Y"), dl.strftime("%Y-%m-%d")

email_counter = 142
thread_counter = 91

def next_email_id():
    global email_counter
    email_counter += 1
    return f"em_{email_counter:05d}"

def next_thread_id():
    global thread_counter
    thread_counter += 1
    return f"th_{thread_counter:04d}"

def make_email(thread_id, msg_index, from_name, from_email, subject, body, received_dt, is_reply=False, attachments=None):
    return {
        "email_id": next_email_id(),
        "thread_id": thread_id,
        "message_index": msg_index,
        "from_name": from_name,
        "from_email": from_email,
        "to": "sales@company.com",
        "cc": [],
        "subject": subject,
        "body": body,
        "received_at": iso(received_dt),
        "attachments": attachments or [],
        "is_reply": is_reply
    }

# ---------- Category generators ----------

def gen_enterprise_rfp():
    company = random.choice(ENTERPRISE_COMPANIES)
    name = random_name()
    domain = company.lower().replace(" ", "") + ".co.in"
    budget_lakhs = random.choice([15, 18, 22, 25, 30, 45, 60, 80])
    received = random_date()
    hours_ahead = random.choice([48, 72, 120, 168, 240])
    deadline_display, _ = deadline_str(received, hours_ahead)
    thread_id = next_thread_id()
    body = (f"{company} invites proposals for an enterprise software solution covering multiple locations. "
            f"Indicative budget is Rs. {budget_lakhs} lakhs. Proposals must reach us by {deadline_display}.")
    return make_email(thread_id, 0, name, random_email(name, domain),
                       f"RFP - Enterprise Software Solution", body, received,
                       attachments=[f"RFP_{company.split()[0]}_2026.pdf"])

def gen_psu_tender():
    entity = random.choice(PSU_ENTITIES)
    name = f"{entity.split()[0]} Procurement"
    domain = "gov.in" if "Government" in entity else entity.lower().split()[0] + ".in"
    value_lakhs = random.choice([3, 5, 6.5, 8, 9])
    received = random_date()
    hours_ahead = random.choice([48, 72])
    deadline_display, _ = deadline_str(received, hours_ahead)
    thread_id = next_thread_id()
    body = (f"{entity} invites bids for supply of enterprise software licences. "
            f"Estimated value: Rs. {value_lakhs},00,000. Last date for bid submission: {deadline_display}.")
    return make_email(thread_id, 0, name, random_email(name, domain),
                       f"Tender Notice - Software Licences", body, received,
                       attachments=["Tender_Notice.pdf"])

def gen_smb_enquiry():
    company = random.choice(SMB_COMPANIES)
    name = random_name()
    domain = company.lower().replace(" ", "") + ".in"
    received = random_date()
    thread_id = next_thread_id()
    urgency = random.choice(["Nothing urgent, whenever works.", "Would love to see a demo soon if possible.", "No rush at all."])
    body = f"Hi, we're a small team at {company} exploring your product. Can we get a demo sometime? {urgency}"
    return make_email(thread_id, 0, name, random_email(name, domain),
                       "Quick demo request", body, received)

def gen_marketing_sponsorship():
    event = random.choice(EVENT_NAMES)
    name = random_name()
    domain = event.lower().replace(" ", "") + ".in"
    tier = random.choice(["Gold", "Silver", "Platinum"])
    amount_lakhs = random.choice([2, 3, 4, 5, 6])
    received = random_date()
    hours_ahead = random.choice([24, 48, 72])
    deadline_display, _ = deadline_str(received, hours_ahead)
    thread_id = next_thread_id()
    body = (f"We're finalising sponsors for {event}. {tier} tier is Rs. {amount_lakhs},00,000 and includes a speaking slot. "
            f"We need confirmation by {deadline_display} as we're going to print.")
    return make_email(thread_id, 0, name, random_email(name, domain),
                       "Sponsorship confirmation needed", body, received)

def gen_alliance_proposal():
    company = random.choice(RESELLER_COMPANIES)
    name = random_name()
    domain = company.lower().replace(" ", "") + ".io"
    clients = random.choice([20, 35, 50, 80])
    received = random_date()
    thread_id = next_thread_id()
    body = (f"We'd like to become a reseller/channel partner for your product in our region. "
            f"We already work with {clients}+ clients and believe there's strong synergy for an integration partnership.")
    return make_email(thread_id, 0, name, random_email(name, domain),
                       "Reseller partnership proposal", body, received)

def gen_finance_invoice():
    company = random.choice(VENDOR_COMPANIES)
    name = f"{company} Billing"
    domain = company.lower().replace(" ", "") + ".co.in"
    amount = random.choice([45000, 62000, 89000, 118000, 156000])
    inv_num = f"INV-2026-{random.randint(1000,9999)}"
    days_overdue = random.choice([3, 7, 12, 20])
    received = random_date()
    thread_id = next_thread_id()
    body = (f"Please find attached invoice {inv_num} for Rs. {amount:,} (incl. 18% GST). "
            f"Payment terms were Net 30 and this is now {days_overdue} days overdue.")
    return make_email(thread_id, 0, name, random_email(name, domain),
                       f"Invoice {inv_num} overdue", body, received,
                       attachments=[f"{inv_num}.pdf"])

def gen_spam():
    company = random.choice(SPAM_COMPANIES)
    name = random_name()
    domain = company.lower().replace(" ", "") + ".biz"
    received = random_date()
    thread_id = next_thread_id()
    pitch = random.choice([
        "We do content marketing, PR outreach, and webinar promotion. Free audit attached.",
        "Our team specializes in lead generation, email marketing campaigns, and event promotion.",
        "We've helped 200+ SaaS companies grow their organic traffic and social presence."
    ])
    body = f"Hi, I noticed your website could use some help ranking. {pitch} Interested in a quick 15 min call?"
    return make_email(thread_id, 0, name, random_email(name, domain),
                       "Free audit - boost your visibility", body, received)

def gen_newsletter():
    source = random.choice(NEWSLETTER_SOURCES)
    domain = source.lower().replace(" ", "") + ".com"
    received = random_date()
    thread_id = next_thread_id()
    body = "Here's your weekly roundup of industry news and trends. Unsubscribe anytime."
    return make_email(thread_id, 0, source, f"noreply@{domain}",
                       f"This week in SaaS: trends to watch", body, received)

def gen_ooo_reply(original_thread_id, original_name, original_email, received):
    body = f"I am out of office with limited access to email. For urgent matters please contact my colleague."
    return make_email(original_thread_id, 1, original_name, original_email,
                       "Out of Office", body, received + timedelta(days=2), is_reply=True)

def gen_ambiguous():
    name = random_name()
    domain = "confused-corp.com"
    received = random_date()
    thread_id = next_thread_id()
    body = ("Hi, not sure who to ask, but we might be interested in either a demo, possibly reselling your "
            "product, or maybe sponsoring your next event. Can someone call me?")
    return make_email(thread_id, 0, name, random_email(name, domain),
                       "Question", body, received)

# ---------- Build the dataset with realistic proportions ----------

emails = []

for _ in range(45): emails.append(gen_enterprise_rfp())
for _ in range(12): emails.append(gen_psu_tender())
for _ in range(60): emails.append(gen_smb_enquiry())
for _ in range(25): emails.append(gen_marketing_sponsorship())
for _ in range(18): emails.append(gen_alliance_proposal())
for _ in range(30): emails.append(gen_finance_invoice())
for _ in range(28): emails.append(gen_spam())
for _ in range(12): emails.append(gen_newsletter())
for _ in range(10): emails.append(gen_ambiguous())

# Add 10 out-of-office replies to some existing enterprise threads
enterprise_originals = [e for e in emails if e["subject"].startswith("RFP")][:10]
for orig in enterprise_originals:
    received_dt = datetime.fromisoformat(orig["received_at"][:19])
    emails.append(gen_ooo_reply(orig["thread_id"], orig["from_name"], orig["from_email"], received_dt))

# Shuffle so categories aren't grouped together (more realistic)
random.shuffle(emails)

print(f"Total emails generated: {len(emails)}")

with open("inbox_250.json", "w", encoding="utf-8") as f:
    json.dump(emails, f, indent=2, ensure_ascii=False)

print("Saved to inbox_250.json")
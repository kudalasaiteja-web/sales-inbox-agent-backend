import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

TEAM_ROSTER = """
- u_aarti (Aarti Menon, Sales — Enterprise): RFPs, RFIs, tenders, and inbound deals above ₹10,00,000
- u_rohit (Rohit Sharma, Sales — SMB): Product enquiries, demo requests, deals at or below ₹10,00,000
- u_meera (Meera Iyer, Marketing): Webinars, event and conference sponsorships, content collaborations, PR and media
- u_karan (Karan Doshi, Alliances): Reseller, channel partner, and technology integration proposals
- u_divya (Divya Rao, Finance): Invoices, purchase orders, payment reminders, GST and vendor billing
- u_triage (Triage Queue, Operations): Ambiguous items requiring human review
"""

ROUTING_RULES = """
Rules (apply in this order — later rules override earlier ones when they conflict):
1. Any email with a stated deadline within 72 hours of received_at gets priority "high", regardless of who it's assigned to.
2. Government and PSU tenders ALWAYS go to u_aarti, no matter the deal value — this overrides the value-based rule below.
3. Deals above ₹10,00,000 (10 lakhs) go to u_aarti (enterprise). Deals at or below ₹10,00,000, or with no stated value, go to u_rohit (SMB) — but ONLY if it's a genuine sales enquiry, not marketing, finance, or alliances content.
4. Event sponsorships, webinars, and content/PR collaborations go to u_meera — even if a monetary amount is mentioned. Money involved does NOT automatically mean Sales.
5. Reseller, channel partner, and technology integration proposals go to u_karan — even if they mention clients or revenue, this is NOT a direct deal.
6. Invoices, POs, payment reminders, and GST/billing queries go to u_divya. The invoice amount is NOT a deal_value_inr — leave deal_value_inr null for these.
7. Do NOT create a task at all for: out-of-office auto-replies, newsletters, or unsolicited vendor spam/cold outreach selling something TO us (as opposed to someone buying from us). Pay close attention to direction of intent — spam often uses marketing-sounding language (webinar, content, PR) but is selling services to us, not asking us for something.
8. If an email is genuinely ambiguous, covers two distinct asks for two different people, or doesn't cleanly fit any category, route it to u_triage with a lower confidence score and explain why in the description.
9. Never fabricate due_date, deal_value_inr, or company_name. If the email doesn't clearly state it, use null. Do not infer a company name from an email domain unless it's unambiguous.
10. Parse Indian numeric shorthand: "lakhs" = x00,000, "crore"/"cr" = x0,000,000. E.g. "25 lakhs" = 2500000, "1.2 cr" = 12000000.
"""

def build_prompt(email: dict) -> str:
    return f"""You are an email routing assistant for a B2B sales inbox. Read the email below and decide how it should be routed.

TEAM AND SCOPES:
{TEAM_ROSTER}

ROUTING RULES:
{ROUTING_RULES}

EMAIL TO CLASSIFY:
From: {email.get('from_name')} <{email.get('from_email')}>
Subject: {email.get('subject')}
Received at: {email.get('received_at')}
Is reply: {email.get('is_reply')}
Body:
{email.get('body')}

Respond with ONLY a JSON object (no markdown, no explanation outside the JSON) in exactly this shape:

{{
  "should_create_task": true or false,
  "skip_reason": "out_of_office" or "newsletter" or "spam" or null (only if should_create_task is false),
  "assignee_id": "u_aarti" | "u_rohit" | "u_meera" | "u_karan" | "u_divya" | "u_triage" (null if should_create_task is false),
  "category": "enterprise_rfp" | "smb_enquiry" | "marketing" | "alliances" | "finance" | "triage" (null if should_create_task is false),
  "priority": "high" | "medium" | "low" (null if should_create_task is false),
  "due_date": "YYYY-MM-DD" or null,
  "deal_value_inr": integer or null,
  "company_name": "string" or null,
  "confidence": float between 0.0 and 1.0,
  "title": "short task title" (null if should_create_task is false),
  "description": "1-2 sentence reasoning, especially important for triage or edge cases"
}}
"""

def classify_email(email: dict) -> dict:
    prompt = build_prompt(email)
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )
    text = response.text.strip()

    # Gemini sometimes wraps JSON in ```json ... ``` — strip that if present
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    return json.loads(text)
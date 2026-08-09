from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel
import uuid

from database import init_db, tasks_collection
from models import TaskCreate, AssigneeId, Category, Priority
from routing import classify_email, client

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    # Step 1: check for a duplicate (same candidate + same source email)
    existing = tasks_collection.find_one({
        "candidate_id": task.candidate_id,
        "source_email_id": task.source_email_id
    })
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Task already exists for source_email_id={task.source_email_id}"
        )

    # Step 2: build the task record
    task_id = "tsk_" + uuid.uuid4().hex[:8]
    created_at = datetime.now(timezone.utc).isoformat()

    task_doc = task.dict()
    task_doc["task_id"] = task_id
    task_doc["created_at"] = created_at

    # Step 3: save it
    tasks_collection.insert_one(task_doc)

    # Step 4: respond in the exact shape your assignment spec requires (§5.1)
    return {
        "task_id": task_id,
        "candidate_id": task.candidate_id,
        "source_email_id": task.source_email_id,
        "created_at": created_at
    }


@app.get("/tasks")
def list_tasks(
    candidate_id: str,
    thread_id: Optional[str] = None,
    source_email_id: Optional[str] = None,
    assignee_id: Optional[str] = None
):
    query = {"candidate_id": candidate_id}
    if thread_id:
        query["thread_id"] = thread_id
    if source_email_id:
        query["source_email_id"] = source_email_id
    if assignee_id:
        query["assignee_id"] = assignee_id

    results = list(tasks_collection.find(query, {"_id": 0}))
    return results


@app.get("/users")
def list_users():
    return {
        "team": [
            {"user_id": "u_aarti", "name": "Aarti Menon", "department": "Sales — Enterprise",
             "scope": "RFPs, RFIs, tenders, and inbound deals above ₹10,00,000"},
            {"user_id": "u_rohit", "name": "Rohit Sharma", "department": "Sales — SMB",
             "scope": "Product enquiries, demo requests, deals at or below ₹10,00,000"},
            {"user_id": "u_meera", "name": "Meera Iyer", "department": "Marketing",
             "scope": "Webinars, event and conference sponsorships, content collaborations, PR and media"},
            {"user_id": "u_karan", "name": "Karan Doshi", "department": "Alliances",
             "scope": "Reseller, channel partner, and technology integration proposals"},
            {"user_id": "u_divya", "name": "Divya Rao", "department": "Finance",
             "scope": "Invoices, purchase orders, payment reminders, GST and vendor billing"},
            {"user_id": "u_triage", "name": "Triage Queue", "department": "Operations",
             "scope": "Ambiguous items requiring human review"}
        ]
    }

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assignee_id: Optional[AssigneeId] = None
    category: Optional[Category] = None
    priority: Optional[Priority] = None
    due_date: Optional[str] = None
    deal_value_inr: Optional[int] = None
    company_name: Optional[str] = None
    confidence: Optional[float] = None


@app.patch("/tasks/{task_id}")
def update_task(task_id: str, updates: TaskUpdate):
    existing = tasks_collection.find_one({"task_id": task_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Task not found")

    # Only include fields the caller actually sent (skip ones left as None)
    update_data = {k: v for k, v in updates.dict().items() if v is not None}

    if update_data:
        tasks_collection.update_one({"task_id": task_id}, {"$set": update_data})

    updated = tasks_collection.find_one({"task_id": task_id}, {"_id": 0})
    return updated


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    result = tasks_collection.delete_one({"task_id": task_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"deleted": True, "task_id": task_id}

from routing import classify_email

@app.post("/ingest")
def ingest_emails(payload: dict):
    emails = payload.get("emails", [])
    candidate_id = payload.get("candidate_id")

    if not candidate_id:
        raise HTTPException(status_code=400, detail="candidate_id is required")

    created = 0
    updated = 0
    skipped = 0
    errors = []

    for email in emails:
        email_id = email.get("email_id")
        thread_id = email.get("thread_id")

        try:
            # Idempotency: has this exact email already been processed?
            existing_for_email = tasks_collection.find_one({
                "candidate_id": candidate_id,
                "source_email_id": email_id
            })
            if existing_for_email:
                skipped += 1
                continue

            # Classify with Gemini
            result = classify_email(email)

            if not result.get("should_create_task"):
                skipped += 1
                continue

            # Thread-aware: is there already a task for this thread?
            existing_for_thread = tasks_collection.find_one({
                "candidate_id": candidate_id,
                "thread_id": thread_id
            })

            if existing_for_thread and email.get("is_reply"):
                # Update the existing task instead of creating a duplicate
                update_fields = {
                    k: result[k] for k in
                    ["title", "description", "assignee_id", "category", "priority",
                     "due_date", "deal_value_inr", "company_name", "confidence"]
                    if result.get(k) is not None
                }
                if update_fields:
                    tasks_collection.update_one(
                        {"task_id": existing_for_thread["task_id"]},
                        {"$set": update_fields}
                    )
                updated += 1
            else:
                # Create a new task
                task_id = "tsk_" + uuid.uuid4().hex[:8]
                created_at = datetime.now(timezone.utc).isoformat()
                task_doc = {
                    "task_id": task_id,
                    "candidate_id": candidate_id,
                    "source_email_id": email_id,
                    "thread_id": thread_id,
                    "title": result.get("title"),
                    "description": result.get("description"),
                    "assignee_id": result.get("assignee_id"),
                    "category": result.get("category"),
                    "priority": result.get("priority"),
                    "due_date": result.get("due_date"),
                    "deal_value_inr": result.get("deal_value_inr"),
                    "company_name": result.get("company_name"),
                    "confidence": result.get("confidence"),
                    "created_at": created_at
                }
                tasks_collection.insert_one(task_doc)
                created += 1

        except Exception as e:
            errors.append({"email_id": email_id, "error": str(e)})

    return {
        "received": len(emails),
        "created": created,
        "updated": updated,
        "skipped": skipped,
        "errors": errors
    }

@app.get("/api/stats")
def get_stats(candidate_id: str):
    all_tasks = list(tasks_collection.find({"candidate_id": candidate_id}, {"_id": 0}))

    total = len(all_tasks)

    by_assignee = {}
    by_category = {}
    by_priority = {}

    for t in all_tasks:
        a = t.get("assignee_id")
        c = t.get("category")
        p = t.get("priority")
        by_assignee[a] = by_assignee.get(a, 0) + 1
        by_category[c] = by_category.get(c, 0) + 1
        by_priority[p] = by_priority.get(p, 0) + 1

    return {
        "total_tasks": total,
        "by_assignee": by_assignee,
        "by_category": by_category,
        "by_priority": by_priority
    }

@app.get("/api/tasks")
def api_list_tasks(candidate_id: str):
    all_tasks = list(
        tasks_collection.find({"candidate_id": candidate_id}, {"_id": 0})
        .sort("created_at", -1)
    )
    return {"tasks": all_tasks}

class ChatRequest(BaseModel):
    candidate_id: str
    message: str

@app.post("/api/chat")
def chat(req: ChatRequest):
    # Step 1: pull all real task data for this candidate
    all_tasks = list(tasks_collection.find({"candidate_id": req.candidate_id}, {"_id": 0}))

    # Step 2: summarize it compactly so we don't blow up the prompt on 250 tasks
    total = len(all_tasks)
    by_assignee = {}
    by_category = {}
    for t in all_tasks:
        by_assignee[t.get("assignee_id")] = by_assignee.get(t.get("assignee_id"), 0) + 1
        by_category[t.get("category")] = by_category.get(t.get("category"), 0) + 1

    # Include full task details too, so specific questions ("what's the biggest deal") can be answered
    task_summaries = "\n".join([
        f"- [{t.get('task_id')}] {t.get('title')} | assignee: {t.get('assignee_id')} | "
        f"category: {t.get('category')} | priority: {t.get('priority')} | "
        f"deal_value_inr: {t.get('deal_value_inr')} | company: {t.get('company_name')}"
        for t in all_tasks
    ])

    prompt = f"""You are a helpful assistant answering questions about a sales team's task inbox.
Answer ONLY using the data below. If the data doesn't contain the answer, say so clearly — do not make anything up.

SUMMARY:
Total tasks: {total}
By assignee: {by_assignee}
By category: {by_category}

FULL TASK LIST:
{task_summaries}

QUESTION: {req.message}

Give a concise, direct answer.
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return {"answer": response.text.strip()}
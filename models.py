from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

# --- Allowed values (enums), exactly as your assignment spec requires ---

class AssigneeId(str, Enum):
    u_aarti = "u_aarti"
    u_rohit = "u_rohit"
    u_meera = "u_meera"
    u_karan = "u_karan"
    u_divya = "u_divya"
    u_triage = "u_triage"

class Category(str, Enum):
    enterprise_rfp = "enterprise_rfp"
    smb_enquiry = "smb_enquiry"
    marketing = "marketing"
    alliances = "alliances"
    finance = "finance"
    triage = "triage"

class Priority(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"

# --- The shape of a task being CREATED (what POST /tasks accepts) ---

class TaskCreate(BaseModel):
    candidate_id: str
    source_email_id: str
    thread_id: str
    title: str
    description: Optional[str] = None
    assignee_id: AssigneeId
    category: Category
    priority: Priority
    due_date: Optional[str] = None          # format YYYY-MM-DD, or null
    deal_value_inr: Optional[int] = None
    company_name: Optional[str] = None
    confidence: float
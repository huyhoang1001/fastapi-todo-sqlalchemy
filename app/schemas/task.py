from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    summary: str
    description: Optional[str] = None
    status: str = "pending"
    priority: str = "medium"

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    summary: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None

class Task(TaskBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskOut(BaseModel):
    id: int
    goal_id: int
    title: str
    description: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

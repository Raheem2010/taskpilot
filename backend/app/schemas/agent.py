from typing import List, Optional

from pydantic import BaseModel


class TaskSchema(BaseModel):
    title: str
    status: str = "pending"


class MilestoneSchema(BaseModel):
    title: str
    description: Optional[str] = None
    tasks: List[TaskSchema] = []


class PlanRequest(BaseModel):
    goal: str


class PlanResponse(BaseModel):
    goal: str
    milestones: List[MilestoneSchema]

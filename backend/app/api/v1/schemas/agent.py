from typing import List, Optional
from pydantic import BaseModel


class TaskSchema(BaseModel):
    id: Optional[int] = None
    title: str
    status: str = "pending"

    class Config:
        from_attributes = True


class MilestoneSchema(BaseModel):
    title: str
    description: Optional[str] = None
    tasks: List[TaskSchema] = []


class PlanRequest(BaseModel):
    goal: str


class PlanResponse(BaseModel):
    goal_id: int
    goal: str
    milestones: List[MilestoneSchema]


class GoalStatusSchema(BaseModel):
    id: int
    goal: str
    status: str
    tasks: List[TaskSchema]

    class Config:
        from_attributes = True


class StatusResponse(BaseModel):
    goals: List[GoalStatusSchema]

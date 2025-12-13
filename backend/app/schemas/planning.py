from datetime import date
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class GoalRequest(BaseModel):
    goal: str = Field(..., min_length=1, description="The user's goal statement")
    deadline: Optional[date] = None
    time_available_per_day: Optional[int] = Field(
        default=None,
        ge=0,
        description="Minutes per day the user can commit (must be non-negative).",
    )


class Milestone(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None


class Task(BaseModel):
    id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1, description="Task title")
    milestone: Optional[str] = None
    duration_minutes: Optional[int] = Field(
        default=None,
        ge=0,
        description="Estimated task duration in minutes (must be non-negative).",
    )
    recommended_day: Optional[date] = None
    status: Literal["pending", "completed", "missed"] = "pending"


class PlanResponse(BaseModel):
    goal: str
    milestones: List[Milestone]
    tasks: List[Task]
    schedule_summary: str


class TaskStatusUpdate(BaseModel):
    task_id: int = Field(..., description="The task ID to update")
    status: Literal["pending", "completed", "missed"]


class TodayTasksResponse(BaseModel):
    date: date
    tasks: List[Task]


class PlanSummaryResponse(BaseModel):
    milestones: List[Milestone]
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    missed_tasks: int


class PlanGenerationRequest(BaseModel):
    goal: str = Field(..., min_length=1, description="The user's goal statement")
    deadline: Optional[date] = None


class PlanGenerationMilestone(BaseModel):
    id: int
    title: str
    due: Optional[date] = None
    tasks: List[str]


class PlanGenerationResponse(BaseModel):
    goal: str
    deadline: Optional[date] = None
    milestones: List[PlanGenerationMilestone]

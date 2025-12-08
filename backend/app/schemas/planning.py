from datetime import date
from typing import List, Optional, Literal

from pydantic import BaseModel


class GoalRequest(BaseModel):
    goal: str
    deadline: Optional[date] = None
    time_available_per_day: Optional[int] = None  # minutes per day


class Milestone(BaseModel):
    title: str
    description: str


class Task(BaseModel):
    id: str
    task: str
    milestone: Optional[str] = None
    duration_minutes: Optional[int] = None
    recommended_day: Optional[date] = None
    status: Literal["pending", "completed", "missed"] = "pending"


class PlanResponse(BaseModel):
    milestones: List[Milestone]
    tasks: List[Task]
    schedule_summary: str


class TaskStatusUpdate(BaseModel):
    task_id: str
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

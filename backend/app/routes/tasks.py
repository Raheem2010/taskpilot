from datetime import date
from typing import Dict

from fastapi import APIRouter, HTTPException, status

from app.schemas.planning import (
    Task,
    TaskStatusUpdate,
    TodayTasksResponse,
    PlanSummaryResponse,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Simple in-memory storage for now (MVP).
FAKE_TASKS_DB: Dict[str, Task] = {}


@router.get("/today", response_model=TodayTasksResponse)
async def get_today_tasks() -> TodayTasksResponse:
    """
    Return tasks for 'today'.

    Currently returns all tasks in the fake DB with today's date
    as the recommended_day if not set.
    """
    today = date.today()

    tasks = []
    for task in FAKE_TASKS_DB.values():
        if task.recommended_day is None or task.recommended_day == today:
            tasks.append(task)

    return TodayTasksResponse(
        date=today,
        tasks=tasks,
    )


@router.post("/update-status", status_code=status.HTTP_201_CREATED)
async def update_task_status(payload: TaskStatusUpdate) -> dict:
    """
    Update the status of a given task.

    For now, this operates on the in-memory FAKE_TASKS_DB.
    """

    task = FAKE_TASKS_DB.get(payload.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = payload.status  # type: ignore[assignment]
    FAKE_TASKS_DB[task.id] = task

    return {
        "message": "Task status updated",
        "task_id": payload.task_id,
        "status": payload.status,
    }


@router.get("/plan-summary", response_model=PlanSummaryResponse)
async def get_plan_summary() -> PlanSummaryResponse:
    """
    Return a simple summary of the current plan based on FAKE_TASKS_DB.
    """

    tasks = list(FAKE_TASKS_DB.values())
    total = len(tasks)
    completed = len([t for t in tasks if t.status == "completed"])
    missed = len([t for t in tasks if t.status == "missed"])
    pending = len([t for t in tasks if t.status == "pending"])

    # Milestones aren't tracked in this fake DB yet; we return an empty list for now.
    return PlanSummaryResponse(
        milestones=[],
        total_tasks=total,
        completed_tasks=completed,
        pending_tasks=pending,
        missed_tasks=missed,
    )

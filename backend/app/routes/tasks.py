from datetime import date
from typing import Dict

from fastapi import APIRouter, HTTPException, status

from app.schemas.planning import (PlanSummaryResponse, Task, TaskStatusUpdate,
                                  TodayTasksResponse)

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Simple in-memory storage for now (MVP).
FAKE_TASKS_DB: Dict[str, Task] = {}


@router.get("/today", response_model=TodayTasksResponse)
async def get_today_tasks() -> TodayTasksResponse:
    """
    Return tasks whose recommended_day is today or not set.
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


@router.patch("/update-status", status_code=status.HTTP_200_OK)
async def update_task_status(payload: TaskStatusUpdate) -> Dict[str, str]:
    """
    Update the status of a given task.
    For now, this operates on the in-memory FAKE_TASKS_DB.
    """
    task = FAKE_TASKS_DB.get(payload.task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_task = task.model_copy(update={"status": payload.status})
    FAKE_TASKS_DB[payload.task_id] = updated_task

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
    completed = missed = pending = 0

    for t in tasks:
        if t.status == "completed":
            completed += 1
        elif t.status == "missed":
            missed += 1
        elif t.status == "pending":
            pending += 1

    # Milestones aren't tracked in this fake DB yet; we return an empty list for now.
    return PlanSummaryResponse(
        milestones=[],
        total_tasks=total,
        completed_tasks=completed,
        pending_tasks=pending,
        missed_tasks=missed,
    )

from fastapi import APIRouter
from app.api.v1.schemas.agent import (
    PlanRequest,
    PlanResponse,
    MilestoneSchema,
    TaskSchema,
)

router = APIRouter(prefix="/plan", tags=["agent"])


@router.post("", response_model=PlanResponse)
async def generate_plan(payload: PlanRequest):
    goal = payload.goal

    milestones = [
        MilestoneSchema(
            title="Clarify and scope your goal",
            description="Define what 'success' means for this goal and set a realistic timeline.",
            tasks=[
                TaskSchema(title="Write a clear one-sentence goal statement"),
                TaskSchema(title="Define 2–3 success metrics"),
            ],
        ),
        MilestoneSchema(
            title="Break goal into weekly tasks",
            description="Create a breakdown of tasks and group them into weekly batches.",
            tasks=[
                TaskSchema(title="List all sub-tasks needed to reach your goal"),
                TaskSchema(title="Group the tasks by week and priority"),
            ],
        ),
        MilestoneSchema(
            title="Set up a tracking system",
            description="Choose how you will track progress (TaskPilot, Notion, spreadsheet, etc.).",
            tasks=[
                TaskSchema(title="Pick a tracking tool and create a project board"),
                TaskSchema(title="Set aside weekly review time in your calendar"),
            ],
        ),
    ]

    return PlanResponse(goal=goal, milestones=milestones)

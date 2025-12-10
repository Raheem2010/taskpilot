from datetime import date, timedelta
from typing import List

from fastapi import APIRouter

from app.schemas.planning import (PlanGenerationMilestone,
                                  PlanGenerationResponse, PlanRequest)

router = APIRouter(tags=["Planning"])


@router.post("/plan", response_model=PlanGenerationResponse)
async def generate_plan(payload: PlanRequest) -> PlanGenerationResponse:
    """
    Simple dummy planner that turns a goal + deadline into 2 milestones.
    """

    mid_deadline = None
    if payload.deadline:
        days_diff = (payload.deadline - date.today()).days
        mid_deadline = date.today() + timedelta(days=days_diff // 2)

    milestones: List[PlanGenerationMilestone] = [
        PlanGenerationMilestone(
            id=1,
            title="Understand & scope the goal",
            due=mid_deadline,
            tasks=[
                f"Clarify requirements for: {payload.goal}",
                "Agree on success criteria with the team",
                "Define constraints, tools and target users",
            ],
        ),
        PlanGenerationMilestone(
            id=2,
            title="Execute and ship MVP",
            due=payload.deadline,
            tasks=[
                "Design backend routes & data flow",
                "Build frontend UI + connect to backend",
                "Test end-to-end and prepare demo pitch",
            ],
        ),
    ]

    return PlanGenerationResponse(
        goal=payload.goal,
        deadline=payload.deadline,
        milestones=milestones,
    )

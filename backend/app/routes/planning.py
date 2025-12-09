from datetime import date
from typing import List

from fastapi import APIRouter

from app.schemas.planning import PlanRequest, PlanResponse, Milestone

router = APIRouter(tags=["Planning"])


@router.post("/plan", response_model=PlanResponse)
async def generate_plan(payload: PlanRequest) -> PlanResponse:
    """
    Simple dummy planner that turns a goal + deadline into 2 milestones.
    Later we can swap this logic for a real LLM/agentic planner.
    """
    # Basic "AI-style" plan using the goal text
    milestones: List[Milestone] = [
        Milestone(
            id=1,
            title="Understand & scope the goal",
            due=payload.deadline,
            tasks=[
                f"Clarify requirements for: {payload.goal}",
                "Agree on success criteria with the team",
                "Define constraints, tools and target users",
            ],
        ),
        Milestone(
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

    return PlanResponse(
        goal=payload.goal,
        deadline=payload.deadline,
        milestones=milestones,
    )

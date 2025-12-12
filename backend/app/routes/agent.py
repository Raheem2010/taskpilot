from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app import models

router = APIRouter(
    prefix="/agent",  
    tags=["agent"],
)


class AgentExecuteRequest(BaseModel):
    task_id: Optional[int] = None
    goal_id: Optional[int] = None
    instruction: Optional[str] = None


class AgentExecuteResponse(BaseModel):
    execution_id: str
    message: str


@router.post("/execute", response_model=AgentExecuteResponse)
def execute_agent(
    payload: AgentExecuteRequest,
    db: Session = Depends(get_db),
):
    """
    Central endpoint for triggering the 'agent' (Cline / automation).

    - If task_id is provided: work on that specific task.
    - Else if goal_id is provided: work on the goal in general.
    - Else: 400.
    """
    if payload.task_id is not None and payload.goal_id is not None:
        raise HTTPException(
            status_code=400,
            detail="Provide either task_id or goal_id, not both.",
        )

    instruction: str

    if payload.task_id is not None:
        task = db.query(models.Task).get(payload.task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # Base instruction: you can refine later
        instruction = payload.instruction or f"Work on task: {task.title}"


    elif payload.goal_id is not None:
        goal = db.query(models.Goal).get(payload.goal_id)
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")

        instruction = payload.instruction or f"Work on goal: {goal.goal}"


    else:
        raise HTTPException(
            status_code=400,
            detail="Either task_id or goal_id must be provided.",
        )

    # TODO: here is where you actually integrate with Cline / automation.
    # For Day 4, we just return a fake execution_id.
    execution_id = f"exec_{payload.task_id or payload.goal_id}"

    return AgentExecuteResponse(
        execution_id=execution_id,
        message=f"Agent started with instruction: {instruction}",
    )

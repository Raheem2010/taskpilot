from app.api.v1.schemas.agent import (
    GoalStatusSchema,
    MilestoneSchema,
    PlanRequest,
    PlanResponse,
    StatusResponse,
    TaskSchema,
)
from app.database import get_db
from app.models.agent import Goal, Task
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

router = APIRouter(tags=["agent"])


@router.post("/plan", response_model=PlanResponse)
async def generate_plan(
    payload: PlanRequest, db: Session = Depends(get_db)
) -> PlanResponse:
    goal_text = payload.goal

    # 1) Create Goal row in DB
    db_goal = Goal(goal=goal_text, status="in_progress")
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)

    # 2) Define milestones + tasks (static for now)
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
                TaskSchema(title="Group tasks by week and priority"),
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

    # 3) Save each task in DB for this goal
    for m in milestones:
        for t in m.tasks:
            db_task = Task(goal_id=db_goal.id, title=t.title, status=t.status)
            db.add(db_task)
    db.commit()

    # 4) Reload tasks from DB and assign IDs in creation order
    db.refresh(db_goal)
    db_tasks = list(db_goal.tasks)
    task_idx = 0

    for m in milestones:
        for t in m.tasks:
            if task_idx < len(db_tasks):
                t.id = db_tasks[task_idx].id
                task_idx += 1

    return PlanResponse(goal_id=db_goal.id, goal=db_goal.goal, milestones=milestones)


@router.get("/status", response_model=StatusResponse)
async def get_status(
    goal_id: int | None = Query(None, description="Optional goal id to filter by"),
    db: Session = Depends(get_db),
):
    """
    Return the current status of goals + tasks from the database.
    """
    query = db.query(Goal)

    if goal_id is not None:
        query = query.filter(Goal.id == goal_id)

    goals = query.order_by(Goal.created_at.desc()).all()

    result_goals: list[GoalStatusSchema] = []

    for g in goals:
        tasks = [
            TaskSchema(
                id=t.id,
                title=t.title,
                status=t.status,
            )
            for t in g.tasks
        ]

        result_goals.append(
            GoalStatusSchema(
                id=g.id,
                goal=g.goal,
                status=g.status,
                tasks=tasks,
            )
        )

    return StatusResponse(goals=result_goals)

from fastapi import APIRouter
from app.routes import goals, tasks, planning, agent  

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(goals.router)
api_router.include_router(tasks.router)
api_router.include_router(planning.router)
api_router.include_router(agent.router)   
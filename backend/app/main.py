import psycopg
from app import models
from app.api.v1.routes.agent import router as agent_router
from app.database import Base, engine
from app.models import agent
from app.routes import goals, planning, tasks
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

app = FastAPI(
    title="TaskPilot Backend",
    version="0.1.0",
    description="Backend API for TaskPilot - AI-powered task planning and workflow automation.",
)

# ❗ For now, we'll let Alembic create tables

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.on_event("startup")
async def verify_db_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise


@app.get("/")
def read_root():
    return {"message": "Welcome to TaskPilot API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(goals.router)
app.include_router(tasks.router)
app.include_router(planning.router)
app.include_router(agent_router, prefix="/api/v1")

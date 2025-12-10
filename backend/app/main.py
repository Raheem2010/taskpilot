from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.routes import tasks, goals, planning 
from app.api.v1.routes.agent import router as agent_router
import psycopg
from app.database import Base, engine
from app.models import agent  

app = FastAPI(
    title="TaskPilot Backend",
    version="0.1.0",
    description="Backend API for TaskPilot - AI-powered task planning and workflow automation."
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


try:
    from psycopg.rows import dict_row
    conn = psycopg.connect(host='localhost', dbname='postgres', user='postgres', password='1984152099')
    cursor = conn.cursor(row_factory=dict_row)
    print("Database connection was successful!")
except Exception as e:
    print("Connecting to database failed")
    print("Error:", e)


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
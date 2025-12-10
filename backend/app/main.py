from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.routes import tasks, goals, planning 
from app.api.v1.routes.agent import router as agent_router

app = FastAPI(
    title="TaskPilot Backend",
    version="0.1.0",
    description="Backend API for TaskPilot - AI-powered task planning and workflow automation."
)

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
from fastapi import FastAPI

app = FastAPI(
    title="TaskPilot Backend",
    version="0.1.0",
    description="Backend API for TaskPilot - AI-powered task planning and workflow automation."
)

@app.get("/")
def read_root():
    return {"message": "Welcome to TaskPilot API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Kestra – TaskPilot Automation

This folder contains the local Kestra setup used by TaskPilot to run automation workflows.

Kestra is run in **standalone mode** with **basic authentication enabled** and is triggered programmatically by the TaskPilot backend.

---

## Folder Structure

- `docker-compose.yml` — Runs Kestra locally in standalone mode
- `.env_encoded` — Local env vars (NOT committed)
- `.env` — Optional local env file (NOT committed)
- `.env.example` — Example env file (safe to commit)
- `kestra-data/` — Kestra local storage volume (NOT committed)

---

## Prerequisites

- Docker Desktop installed and running
- Docker Compose enabled

---

## Setup

### 1) Create your local env file

Copy the example file:

**Windows (PowerShell)**
```powershell
Copy-Item .env.example .env_encoded
Windows (CMD)

cmd
Copy code
copy .env.example .env_encoded
Then edit .env_encoded and set your values.

⚠️ Do not commit .env or .env_encoded.

2) Start Kestra
From the kestra/ directory:

bash
Copy code
docker compose up -d
Kestra exposes the UI and API on port 8080.

3) Access Kestra UI
URL: http://localhost:8080

Username: taskpilot@local.test

Password: Taskpilot123

4) Health check
bash
Copy code
curl http://localhost:8080/api/v1/health
Expected response:

json
Copy code
{ "status": "UP" }
How TaskPilot Uses Kestra
TaskPilot triggers workflows through:

text
Copy code
POST /api/v1/main/executions
This call is made only from the backend.
The CLI and frontend never call Kestra directly.

Authentication
Kestra is secured using basic authentication. The backend must send valid credentials.

Backend environment variables
Set these in the backend environment:

env
Copy code
KESTRA_BASE_URL=http://localhost:8080
KESTRA_UI_URL=http://localhost:8080
KESTRA_NAMESPACE=main
KESTRA_FLOW_ID=<flow_id>
KESTRA_USERNAME=taskpilot@local.test
KESTRA_PASSWORD=Taskpilot123
Stopping and Resetting
Stop containers:

bash
Copy code
docker compose down
Reset local Kestra data (removes execution history):

bash
Copy code
docker compose down -v
Security Notes (Local Dev Only)
The Docker socket mount (/var/run/docker.sock) grants host-level Docker access. This is acceptable for local development but must not be used in production.

Credentials shown here are for local development only and should be replaced in production.
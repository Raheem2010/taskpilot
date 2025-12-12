# Kestra – TaskPilot Automation

This folder contains the local Kestra setup used by TaskPilot to run automation workflows.

Kestra is run in **standalone mode** with **basic authentication enabled** and is triggered programmatically by the TaskPilot backend.

---

## Folder Structure

- `docker-compose.yml` — Runs Kestra locally in standalone mode
- `.env_encoded` — Encoded/local environment variables (NOT committed)
- `.env` — Optional local env file (NOT committed)
- `.env.example` — Example env file (safe to commit)
- `kestra-data/` — Kestra local storage volume (NOT committed)

---

## Prerequisites

- Docker Desktop installed and running
- Docker Compose enabled

---

## Setup Instructions

### 1️⃣ Create environment file

Copy the example file:

**Windows (PowerShell)**
```powershell
Copy-Item .env.example .env_encoded
Windows (CMD)

cmd
Copy code
copy .env.example .env_encoded
Then update .env_encoded with your local values.

⚠️ Do not commit .env or .env_encoded.

2️⃣ Start Kestra
From the kestra/ directory:

bash
Copy code
docker compose up -d
Kestra will start in standalone mode and expose the UI and API on port 8080.

3️⃣ Access Kestra UI
URL: http://localhost:8080

Username: taskpilot@local.test

Password: Taskpilot123

4️⃣ Health Check
bash
Copy code
curl http://localhost:8080/api/v1/health
Expected response:

json
Copy code
{ "status": "UP" }
How TaskPilot Uses Kestra
TaskPilot triggers automation workflows by calling the Kestra API endpoint:

bash
Copy code
POST /api/v1/main/executions
This call is made only from the backend.
The CLI and frontend never call Kestra directly.

Authentication
Kestra is secured using basic authentication.
The backend must send valid credentials when triggering executions.

Required Backend Environment Variables
The backend must be configured with:

KESTRA_BASE_URL=http://localhost:8080

KESTRA_NAMESPACE=main

KESTRA_FLOW_ID=<flow_id>

KESTRA_USERNAME=taskpilot@local.test

KESTRA_PASSWORD=Taskpilot123

Stopping and Resetting Kestra
Stop containers:

bash
Copy code
docker compose down
Stop and remove all local Kestra data:

bash
Copy code
docker compose down -v
Troubleshooting
401 Unauthorized
Ensure the backend is sending basic auth credentials

Confirm the username/password match those in docker-compose.yml

Do not mix basic auth with token auth

Cannot reach Kestra from backend
From host machine: use http://localhost:8080

From another Docker container: use http://kestra:8080

Executions trigger but do not appear
Confirm namespace is main

Confirm flow ID exists in Kestra

Check logs:

bash
Copy code
docker compose logs -f kestra

NOTE:
Kestra credentials shown in this repository are for local development only and are not used in production.

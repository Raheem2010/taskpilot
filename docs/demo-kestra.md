## 🤖 Automation Demo — Daily Review Agent (Kestra)

This demo shows how TaskPilot triggers an AI automation workflow using **Kestra**.

---

## Prerequisites
- Docker & Docker Compose installed
- Backend running on `http://localhost:8000`
- Kestra running on `http://localhost:8080`

---

## 1️⃣ Start Kestra

```bash
cd kestra
docker compose up -d
Open the Kestra UI:

arduino
Copy code
http://localhost:8080
2️⃣ Verify the Flow Exists
Ensure the flow taskpilot_ai_agent exists in the main namespace.

In the Kestra UI:
Flows → main → taskpilot_ai_agent
Kestra Flow Loaded

![Kestra Flow](./screenshots/kestra_flow.png)

3️⃣ Trigger Automation from Backend
Run the backend-triggered automation:

bash
curl -X POST http://localhost:8000/api/v1/automation/daily-review
Expected response:

json
{
  "message": "Kestra daily-review flow triggered",
  "execution_id": "...",
  "kestra_url": "http://localhost:8080/ui/executions/main/taskpilot_ai_agent/<id>"
}
Backend Trigger Response
![Backend Trigger](./screenshots/backend-response.png)


4️⃣ View Execution in Kestra
Open the returned kestra_url in your browser to view:

Flow execution

Input values

Execution logs

Kestra Execution View
![Kestra Execution](./screenshots/kestra1_succes-Execution.png)



Kestra Logs
![Kestra Log](./screenshots/kestra_log.png)


5️⃣ (Optional) Manual Execution from UI
You can also execute the flow manually via the Kestra UI by providing:

goal

source

reason

This is useful for live demos and screenshots.

✅ Result
TaskPilot successfully triggers an automated workflow via Kestra, proving:

Backend → automation orchestration

Reliable event-based execution

Extensible AI agent pipeline using Kestra
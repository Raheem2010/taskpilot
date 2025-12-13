import os

import httpx
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/automation", tags=["Automation"])

KESTRA_BASE_URL = os.getenv("KESTRA_BASE_URL", "http://localhost:8080").rstrip("/")
KESTRA_UI_URL = os.getenv("KESTRA_UI_URL", KESTRA_BASE_URL).rstrip("/")

KESTRA_TENANT = os.getenv("KESTRA_TENANT", "main")

KESTRA_NAMESPACE = os.getenv("KESTRA_NAMESPACE", "main")
KESTRA_FLOW_ID = os.getenv("KESTRA_FLOW_ID", "taskpilot_ai_agent")

KESTRA_USERNAME = os.getenv("KESTRA_USERNAME")
KESTRA_PASSWORD = os.getenv("KESTRA_PASSWORD")


@router.post("/daily-review")
async def trigger_daily_review():
   
    if not KESTRA_USERNAME or not KESTRA_PASSWORD:
        raise HTTPException(status_code=500, detail="Kestra credentials not configured")

    
    url = f"{KESTRA_BASE_URL}/api/v1/{KESTRA_TENANT}/executions/{KESTRA_NAMESPACE}/{KESTRA_FLOW_ID}"

    
    multipart_fields = {
        "goal": (None, "Daily review"),
        "source": (None, "backend"),
        "reason": (None, "daily-review"),
    }

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(
                url,
                auth=(KESTRA_USERNAME, KESTRA_PASSWORD),
                files=multipart_fields,
            )
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail="Error connecting to Kestra") from e

    if resp.status_code >= 300:
        raise HTTPException(
            status_code=502,
            detail=f"Kestra call failed (status={resp.status_code}).",
        )

    try:
        data = resp.json()
    except ValueError as e:
        raise HTTPException(status_code=502, detail="Kestra returned a non-JSON response") from e

    execution_id = data.get("id")
    if not execution_id:
        raise HTTPException(status_code=502, detail="Kestra returned no execution id")

    return {
        "message": "Kestra daily-review flow triggered",
        "execution_id": execution_id,
        "kestra_url": f"{KESTRA_UI_URL}/ui/executions/{KESTRA_NAMESPACE}/{KESTRA_FLOW_ID}/{execution_id}",
    }
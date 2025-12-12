import os
import httpx
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/automation", tags=["Automation"])

KESTRA_BASE_URL = os.getenv("KESTRA_BASE_URL", "http://localhost:8080")
KESTRA_UI_URL = os.getenv("KESTRA_UI_URL", KESTRA_BASE_URL)

KESTRA_NAMESPACE = "taskpilot.ai"
KESTRA_FLOW_ID = "taskpilot_ai_agent"

KESTRA_USERNAME = os.getenv("KESTRA_USERNAME")
KESTRA_PASSWORD = os.getenv("KESTRA_PASSWORD")


@router.post("/daily-review")
async def trigger_daily_review():
    """
    Trigger the Kestra AI agent flow that summarizes tasks
    and optionally marks one as completed.
    """
    if not KESTRA_USERNAME or not KESTRA_PASSWORD:
        raise HTTPException(status_code=500, detail="Kestra credentials not configured")
    
    url = f"{KESTRA_BASE_URL}/api/v1/main/executions/{KESTRA_NAMESPACE}/{KESTRA_FLOW_ID}"


    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                url,
                auth=(KESTRA_USERNAME, KESTRA_PASSWORD),  # Basic Auth
            )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Error connecting to Kestra: {str(e)}",
        )

    if resp.status_code >= 300:
        raise HTTPException(
            status_code=resp.status_code,
            detail=f"Kestra responded with {resp.status_code}: {resp.text}",
        )

    data = resp.json()
    execution_id = data.get("id")
    if not execution_id:
        raise HTTPException(status_code=502, detail=f"Kestra returned no execution id: {data}")


    return {
        "message": "Kestra daily-review flow triggered",
        "execution_id": data.get("id"),
        "kestra_url": (
            f"{KESTRA_UI_URL}/ui/executions/"
            f"{KESTRA_NAMESPACE}/{KESTRA_FLOW_ID}/{execution_id}"
        ),
    }

from typing import Any, Dict, List, Optional

import requests
import typer

from .config import get_full_url

app = typer.Typer(help="TaskPilot CLI – plan and track your goals with AI agents.")


@app.command()
def plan(
    goal: str = typer.Argument(
        ...,
        help="Your main goal, e.g. 'Launch my shoe brand in 3 months'",
    )
):
    """
    Send a goal to TaskPilot backend and get an AI-generated (or dummy) plan: milestones + tasks.
    """
    typer.echo(f"🧠 Planning for goal: {goal}\n")

    url = get_full_url(
        "plan"
    )  # expects POST /api/v1/plan or /plan depending on your config
    payload = {"goal": goal}

    try:
        response = requests.post(url, json=payload)
    except requests.exceptions.RequestException as e:
        typer.secho(f"❌ Failed to contact backend: {e}", err=True)
        raise typer.Exit(code=1)

    if response.status_code != 200:
        typer.secho(
            f"❌ Backend error {response.status_code}:\n{response.text}", err=True
        )
        raise typer.Exit(code=1)

    data: Dict[str, Any] = response.json()
    milestones: List[Dict[str, Any]] = data.get("milestones", [])

    if not milestones:
        typer.echo("⚠️ No milestones returned from backend.")
        typer.echo(f"Raw response: {data}")
        raise typer.Exit(code=0)

    for i, m in enumerate(milestones, start=1):
        title = m.get("title") or f"Milestone {i}"
        desc = m.get("description") or ""

        typer.secho(f"📌 Milestone {i}: {title}", bold=True)
        if desc:
            typer.echo(f"    📝 {desc}")

        tasks = m.get("tasks") or []
        if not tasks:
            typer.echo("    (No tasks defined)")
        else:
            for j, t in enumerate(tasks, start=1):
                if isinstance(t, dict):
                    t_title = t.get("title") or t.get("name") or str(t)
                    t_status = t.get("status", "pending")
                else:
                    t_title = str(t)
                    t_status = "pending"

                typer.echo(f"    - [{t_status:^8}] {t_title}")

        typer.echo("")  # blank line between milestones


@app.command()
def status(
    goal_id: Optional[str] = typer.Option(
        None,
        "--goal-id",
        "-g",
        help="Optional ID of the goal to filter status on.",
    )
):
    """
    Get the current status of your goals/tasks from TaskPilot backend.
    """
    typer.echo("📊 Fetching status from TaskPilot backend...\n")

    url = get_full_url("status")  # we will later implement GET /api/v1/status
    params: Dict[str, Any] = {}

    if goal_id:
        params["goal_id"] = goal_id

    try:
        response = requests.get(url, params=params)
    except requests.exceptions.RequestException as e:
        typer.secho(f"❌ Failed to contact backend: {e}", err=True)
        raise typer.Exit(code=1)

    if response.status_code != 200:
        typer.secho(
            f"❌ Backend error {response.status_code}:\n{response.text}", err=True
        )
        raise typer.Exit(code=1)

    data: Dict[str, Any] = response.json()
    goals: List[Dict[str, Any]] = data.get("goals", [])

    if not goals:
        typer.echo("No goals found yet. Try creating one with `taskpilot plan`.")
        raise typer.Exit(code=0)

    for g in goals:
        gid = g.get("id") or g.get("goal_id") or "N/A"
        title = g.get("title") or g.get("goal") or "Untitled goal"
        status_val = g.get("status") or "unknown"

        typer.secho(f"🎯 Goal: {title}", bold=True)
        typer.echo(f"    ID: {gid}")
        typer.echo(f"    Status: {status_val}")

        tasks = g.get("tasks") or []
        for t in tasks:
            t_title = t.get("title") or t.get("name") or "Untitled task"
            t_status = t.get("status") or "pending"
            typer.echo(f"    - [{t_status:^8}] {t_title}")

        typer.echo("")


def main():
    app()


if __name__ == "__main__":
    main()

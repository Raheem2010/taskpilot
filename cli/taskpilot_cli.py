from typing import Any, Dict, List, Optional

import requests
import typer

from .config import get_full_url
import json

app = typer.Typer(help="TaskPilot CLI – plan and track your goals with AI agents.")



app = typer.Typer(help="TaskPilot CLI")


@app.command()
def plan(
    goal: str = typer.Argument(
        ...,
        help="Your main goal, e.g. 'Launch my shoe brand in 3 months'",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Print raw JSON response instead of pretty text (for automation).",
    ),
) -> None:
    """
    Send a goal to the TaskPilot backend and get a plan (milestones + tasks).
    """

    url = get_full_url("plan")
    payload = {"goal": goal}

    try:
        response = requests.post(url, json=payload, timeout=30)
    except requests.exceptions.RequestException as e:
        typer.secho(f"❌ Failed to contact backend: {e}", err=True, fg=typer.colors.RED)
        raise typer.Exit(code=1) from e

    if response.status_code != 200:
        typer.secho(
            f"❌ Backend returned {response.status_code}: {response.text}",
            err=True,
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    data = response.json()

    # 🔁 Automation mode: raw JSON
    if json_output:
        typer.echo(json.dumps(data, indent=2))
        return

    # 🧑🏽‍💻 Human-readable pretty output
    typer.secho(f"🧠 Planning for goal: {data['goal']}", bold=True)
    typer.echo()

    for idx, milestone in enumerate(data["milestones"], start=1):
        typer.secho(f"📌 Milestone {idx}: {milestone['title']}")
        if milestone.get("description"):
            typer.echo(f"    📝 {milestone['description']}")
        for task in milestone["tasks"]:
            status = task.get("status", "pending")
            typer.echo(f"    - [{status:<8}] {task['title']}")
        typer.echo()


@app.command()
def status(
    goal_id: int = typer.Option(
        None,
        "--goal-id",
        help="Filter by a specific goal ID.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Print raw JSON response instead of pretty text (for automation).",
    ),
) -> None:
    """
    Fetch current goals and tasks from the TaskPilot backend.
    """

    url = get_full_url("status")
    params: dict = {}
    if goal_id is not None:
        params["goal_id"] = goal_id

    try:
        response = requests.get(url, params=params, timeout=30)
    except requests.exceptions.RequestException as e:
        typer.secho(f"❌ Failed to contact backend: {e}", err=True, fg=typer.colors.RED)
        raise typer.Exit(code=1) from e

    if response.status_code != 200:
        typer.secho(
            f"❌ Backend returned {response.status_code}: {response.text}",
            err=True,
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    data = response.json()

    # Automation mode: raw JSON
    if json_output:
        typer.echo(json.dumps(data, indent=2))
        return

    # 🧑🏽‍💻 Human-readable pretty output
    goals = data.get("goals", [])
    if not goals:
        typer.secho("ℹ️ No goals found yet.", fg=typer.colors.YELLOW)
        return

    for goal in goals:
        typer.secho(f"🎯 Goal: {goal['goal']}", bold=True)
        typer.echo(f"    ID: {goal['id']}")
        typer.echo(f"    Status: {goal['status']}")
        tasks = goal.get("tasks", [])
        for task in tasks:
            typer.echo(f"    - [{task['status']:<8}] {task['title']}")
        typer.echo()


@app.command()
def health() -> None:
    """
    Quick health check: verify that the TaskPilot backend is reachable.
    """
    url = get_full_url("health")

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        typer.secho(
            f"❌ Backend health check failed: {e}",
            err=True,
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1) from e

    if response.status_code != 200:
        typer.secho(
            f"❌ Backend unhealthy: {response.status_code} -> {response.text}",
            err=True,
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    typer.secho(
        "✅ Backend is healthy and reachable!",
        fg=typer.colors.GREEN,
        bold=True,
    )


def main():
    app()


if __name__ == "__main__":
    main()

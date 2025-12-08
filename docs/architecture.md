# 🧱 TaskPilot – System Architecture

This document describes the high-level architecture of **TaskPilot**, showing how the frontend, backend, workflows, and AI agents interact.

---

## 1. High-Level Overview

TaskPilot is composed of the following core components:

- **Frontend (Next.js on Vercel)**  
  - Provides the user interface (goal input, task view, replan button).
  - Communicates with the backend over HTTP (REST API).

- **Backend (FastAPI – Python)**  
  - Central coordinator between the frontend, Kestra workflows, and AI agents.
  - Exposes API endpoints for goals, tasks, and plan summaries.
  - Triggers Kestra workflows and consumes their results.
  - Stores and retrieves planning data (in-memory or DB, depending on phase).

- **Workflow Orchestrator (Kestra)**  
  - Defines and runs workflows for:
    - Planning goals (calling AI agent).
    - Sending daily reminders.
    - Adaptive re-planning when tasks are missed.
  - Communicates back to the backend via HTTP or callbacks.

- **AI Agents (Oumi)**  
  - GoalPlannerAgent: turns user goals into milestones and tasks.
  - AdaptiveReplanAgent (optional): adjusts plans when progress changes.
  - Accessed from Kestra workflows or the backend via HTTP/API.

- **Developer Tools**
  - **Cline**: used locally in the IDE to assist coding and refactoring.
  - **CodeRabbit**: performs automated code review on Pull Requests.

---

## 2. Architecture Diagram (Text / ASCII View)

```text
                   ┌─────────────────────────────┐
                   │         User (Browser)      │
                   └──────────────┬──────────────┘
                                  │ HTTP (HTTPS)
                                  │
                     Frontend (Vercel / Next.js)
                   ┌──────────────┴──────────────┐
                   │  Goal input form            │
                   │  Dashboard (tasks, status)  │
                   │  Replan trigger button      │
                   └──────────────┬──────────────┘
                                  │ HTTP API calls
                                  │
                         Backend (FastAPI – Python)
                   ┌──────────────┴──────────────┐
                   │ /goals/plan                 │
                   │ /tasks/today                │
                   │ /tasks/update-status        │
                   │ /plan/summary               │
                   └──────────────┬──────────────┘
                                  │
                                  │ HTTP / REST
                                  │
                        ┌─────────▼─────────┐
                        │   Kestra          │
                        │  Workflows        │
                        └─────────┬─────────┘
                                  │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
             │                    │                    │
   goal_planning.yml    daily_reminder.yml   adaptive_replan.yml
 (call AI agent to       (cron: send        (rebuild plan when
 build initial plan)     reminders)         tasks are missed)

                                  │
                                  │ AI / HTTP call
                                  ▼
                         ┌──────────────────┐
                         │  Oumi AI Agents  │
                         │  (LLM backend)   │
                         └──────────────────┘

3. Data Flow (MVP Scenario)
1. User Creates a Goal

User opens the TaskPilot frontend.

Enters:

Goal description

Deadline (optional)

Time available per day (optional)

Frontend sends POST request to backend:

POST /goals/plan

Backend validates payload and triggers the Kestra goal_planning workflow with the goal data.

Kestra workflow calls Oumi GoalPlannerAgent, which:

Generates milestones

Generates tasks with estimated durations

Suggests a schedule

Kestra returns the structured plan to the backend.

Backend stores the plan (e.g., in-memory or database) and returns it to the frontend.

Frontend displays the plan to the user (tasks + schedule).

2. Daily Reminders

A Kestra cron-based workflow (daily_reminder.yml) runs each morning (e.g., 08:00).

Workflow:

Fetches “today’s tasks” from storage or via backend.

Sends a notification/output:

via HTTP callback to backend,

or via logs / simple UI polling for MVP.

Backend can expose an endpoint to fetch “today’s tasks”:

GET /tasks/today

Frontend shows a “Today” view listing tasks due today.

3. Adaptive Re-Planning

User marks tasks as:

completed

or missed

via:

POST /tasks/update-status

If tasks are marked as missed, backend triggers Kestra adaptive_replan.yml with:

previous tasks

missed tasks

progress context

Kestra calls Oumi AdaptiveReplanAgent to generate an updated, simpler plan.

New plan is saved and returned to the frontend.

Frontend updates the dashboard to show the adjusted schedule.

4. Components & Responsibilities
Frontend (Next.js)

Display goal input and results.

Provide user-friendly dashboard.

Call backend APIs and show responses.

Keep UX clean and “hackathon-demo ready”.

Backend (FastAPI)

Validate and handle HTTP requests.

Trigger Kestra workflows.

Serve task/plan data to the frontend.

Provide integration point for future features (auth, persistence, etc.).

Kestra Workflows

goal_planning.yml:

Input: goal data.

Calls GoalPlannerAgent.

Output: milestones + tasks + schedule.

daily_reminder.yml:

Cron-based.

Finds today’s tasks.

Notifies backend/UI.

adaptive_replan.yml:

Input: missed tasks + progress.

Calls AdaptiveReplanAgent.

Output: updated plan.

AI Agents (Oumi)

Implemented as HTTP-accessible LLM endpoints.

Responsible only for reasoning and content generation, not storage.

Developer Tools

Cline: used in the IDE to speed up coding and refactoring.

CodeRabbit: reviews PRs for code quality, structure, tests, and docs.

5. Future Extensions (Beyond MVP)

Persistent database (PostgreSQL, etc.) for users, goals, and tasks.

User authentication and multi-user support.

Team goals and collaborative task assignment.

Calendar integrations (Google Calendar, Outlook).

Rich notification channels (email, SMS, push notifications).

This architecture is designed to keep TaskPilot simple to reason about, easy to demo, and flexible enough to evolve after the hackathon.

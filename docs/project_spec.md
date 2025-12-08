TaskPilot — Project Structure Documentation

This document explains the folder layout of the TaskPilot project and the purpose of each directory.
The structure is designed for clarity, teamwork, and clean orchestration of backend, frontend, and workflow automation.

1. High-Level Structure
taskpilot/
│
├── backend/
├── frontend/
├── workflows/
├── docs/
└── README.md


Each folder plays a specific role in the TaskPilot system.
Below is a detailed explanation of each.

2. Folder-by-Folder Breakdown
🔹 backend/

Tech: FastAPI (Python)

The backend is the core “brain” that coordinates requests between:

the frontend

the AI agents (Oumi)

Kestra workflows

Expected Internal Structure:
backend/
│
├── app/
│   ├── main.py
│   ├── routes/
│   ├── models/
│   ├── services/
│   └── utils/
│
└── requirements.txt

Purpose:

Expose API routes (e.g., /goals/plan, /tasks/today)

Communicate with Kestra workflows

Store / fetch planning data

Manage user actions (task updates, replanning triggers)

🔹 frontend/

Tech: Next.js (React) → deployed on Vercel

This folder contains all UI/UX components.

Expected Internal Structure:
frontend/
│
├── pages/
├── components/
├── public/
├── hooks/
└── package.json

Purpose:

Capture user goals

Display tasks and progress

Show daily schedule

Provide replan button

Communicate with backend APIs

🔹 workflows/

Tech: Kestra YAML workflow definitions

This is where all automation logic lives.

Expected Files:
workflows/
│
├── goal_planning.yml
├── daily_reminder.yml
└── adaptive_replan.yml

Purpose:

Trigger AI planning workflow

Schedule reminders

Adjust tasks when user falls behind

Log task progress events

Enable end-to-end orchestration of the system

These workflows form the backbone of TaskPilot’s automation.

🔹 docs/

Project documentation, planning files, diagrams, and internal notes.

Expected Files:
docs/
│
├── project_spec.md
├── project_structure.md
└── architecture.png      (optional: will be added later)

Purpose:

Store the full project specification

Store architectural diagrams

Store all internal docs for team coordination

Used for better organization and CodeRabbit review

This folder grows as the project evolves.

🔹 README.md (root)

This is the main documentation that GitHub visitors will see first.
It will include:

Project overview

Features

Architecture diagram

How to run the project

Demo links

Tools used (Cline, Kestra, Vercel, Oumi, CodeRabbit)

Installation instructions

We will update it continuously as the project evolves.

3. Git Workflow Strategy

We recommend using this branching model:

main   → always stable and deployable  
dev    → integration branch for teammates  
feature branches → development work

Example feature branches:

feat/backend-api

feat/frontend-ui

feat/workflows-setup

feat/agent-integration

Every feature branch should create a PR into dev, which triggers CodeRabbit reviews.

After testing, dev is merged into main.

4. Why This Structure Works Well

✔ Clean division between backend, frontend, workflows, and docs
✔ Easy for team members to work independently
✔ Compatible with CodeRabbit’s PR review model
✔ Clear files for judging and hackathon submission
✔ Easy to deploy (Vercel frontend + backend API + YAML workflows)
✔ Scales well as new features are added

5. Summary

This structure ensures:

Maintainability

Clear workflow orchestration

Smooth team collaboration

Fast onboarding

Clean hackathon presentation
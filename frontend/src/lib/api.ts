const BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export type Task = {
  id: number;
  title: string;
  status: string;
};

export type Milestone = {
  title: string;
  description?: string | null;
  tasks: Task[];
};

export type PlanResponse = {
  goal: string;
  goal_id: number;
  milestones: Milestone[];
};

export type StatusTask = {
  id: number;
  title: string;
  status: string;
};

export type StatusGoal = {
  id: number;
  goal: string;
  status: string;
  tasks: StatusTask[];
};

export type StatusResponse = {
  goals: StatusGoal[];
};

export async function createPlan(goal: string): Promise<PlanResponse> {
  const res = await fetch(`${BASE_URL}/api/v1/plan`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ goal }),
  });

  if (!res.ok) {
    const msg = await res.text();
    throw new Error(`Backend error (${res.status}): ${msg}`);
  }

  return res.json();
}

export async function getStatus(goalId?: number): Promise<StatusResponse> {
  const params = goalId ? `?goal_id=${goalId}` : "";
  const res = await fetch(`${BASE_URL}/api/v1/status${params}`);

  if (!res.ok) {
    const msg = await res.text();
    throw new Error(`Backend error (${res.status}): ${msg}`);
  }

  return res.json();
}

export async function healthCheck(): Promise<boolean> {
  const res = await fetch(`${BASE_URL}/health`);
  if (!res.ok) {
    throw new Error("Backend unhealthy");
  }
  return true;
}

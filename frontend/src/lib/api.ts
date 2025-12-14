const RAW_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

const BASE_URL = RAW_BASE_URL.replace(/\/+$/, ""); // remove trailing /

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

async function parseJsonOrThrow<T>(res: Response, url: string): Promise<T> {
  const contentType = res.headers.get("content-type") ?? "";

  // Read body once (safe for both JSON + HTML)
  const bodyText = await res.text();

  if (!res.ok) {
    const preview = bodyText.slice(0, 250);
    throw new Error(`Backend error (${res.status}) @ ${url}: ${preview}`);
  }

  if (!contentType.includes("application/json")) {
    const preview = bodyText.slice(0, 250);
    throw new Error(
      `Non-JSON response @ ${url}. content-type=${contentType}. body=${preview}`
    );
  }

  try {
    return JSON.parse(bodyText) as T;
  } catch {
    const preview = bodyText.slice(0, 250);
    throw new Error(`Invalid JSON @ ${url}: ${preview}`);
  }
}

export async function createPlan(goal: string): Promise<PlanResponse> {
  const url = `${BASE_URL}/api/v1/plan`;
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ goal }),
  });

  return parseJsonOrThrow<PlanResponse>(res, url);
}

export async function getStatus(goalId?: number): Promise<StatusResponse> {
  const params = goalId ? `?goal_id=${goalId}` : "";
  const url = `${BASE_URL}/api/v1/status${params}`;
  const res = await fetch(url);

  return parseJsonOrThrow<StatusResponse>(res, url);
}

export async function healthCheck(): Promise<boolean> {
  const url = `${BASE_URL}/health`;
  const res = await fetch(url);

  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`Backend unhealthy (${res.status}): ${txt.slice(0, 200)}`);
  }
  return true;
}

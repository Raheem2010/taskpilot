"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

const BACKEND_BASE_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export default function HomePage() {
  const router = useRouter();
  const [goal, setGoal] = useState("");
  const [deadline, setDeadline] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
  e.preventDefault();
  setError("");
  setLoading(true);

  try {
    const res = await fetch(`${BACKEND_BASE_URL}/plan`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        goal,
        deadline: deadline || null,
      }),
    });

    if (!res.ok) {
      throw new Error("Failed to generate plan");
    }

    const data = await res.json();

    if (typeof window !== "undefined") {
      window.localStorage.setItem("taskpilot-plan", JSON.stringify(data));
      window.localStorage.setItem("taskpilot-plan-source", "backend");
    }

    router.push("/plan");
  } catch (err) {
    console.error(err);
    setError(err.message || "Something went wrong");
  } finally {
    setLoading(false);
  }
}


  return (
    <section className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold mb-1">
          What do you want your agent to build?
        </h2>
        <p className="text-sm text-slate-400">
          Describe your goal and deadline. TaskPilot will break it into
          milestones and tasks for your team.
        </p>
      </div>

      <form
        onSubmit={handleSubmit}
        className="space-y-4 bg-slate-900/60 border border-slate-800 rounded-2xl p-4"
      >
        <div className="space-y-1">
          <label className="text-sm font-medium">Goal</label>
          <textarea
            className="w-full rounded-xl bg-slate-950 border border-slate-800 px-3 py-2 text-sm outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
            rows={4}
            placeholder="Example: Build an AI agent that automates our GitHub PR review workflow using Cline + CodeRabbit..."
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            required
          />
        </div>

        <div className="space-y-1">
          <label className="text-sm font-medium">Target deadline</label>
          <input
            type="date"
            className="w-full rounded-xl bg-slate-950 border border-slate-800 px-3 py-2 text-sm outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
            value={deadline}
            onChange={(e) => setDeadline(e.target.value)}
          />
        </div>

        {error && (
          <p className="text-sm text-red-400 bg-red-950/30 border border-red-900 rounded-xl px-3 py-2 rounded-xl">
            {error}
          </p>
        )}

        <button
          type="submit"
          disabled={loading}
          className="inline-flex items-center justify-center rounded-xl px-4 py-2 text-sm font-medium bg-indigo-500 hover:bg-indigo-400 disabled:opacity-60 disabled:cursor-not-allowed transition"
        >
          {loading ? "Generating plan..." : "Generate plan"}
        </button>
      </form>
    </section>
  );
}

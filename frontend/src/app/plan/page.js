"use client";

import { useEffect, useState } from "react";

export default function PlanPage() {
  const [plan, setPlan] = useState(null);
  const [source, setSource] = useState("unknown"); // "backend" | "fallback" | "unknown"

  useEffect(() => {
    if (typeof window === "undefined") return;

    const storedPlan = window.localStorage.getItem("taskpilot-plan");
    const storedSource = window.localStorage.getItem("taskpilot-plan-source");

    if (storedPlan) {
      setPlan(JSON.parse(storedPlan));
      setSource(storedSource || "backend");
    } else {
      // Fallback dummy plan if user landed here directly
      setPlan({
        goal: "Demo: Build TaskPilot agentic workflow",
        deadline: null,
        milestones: [
          {
            id: 1,
            title: "Day 1 – Backend & agentic flow",
            due: "2025-12-08",
            tasks: [
              "Design task schema & /plan endpoint",
              "Implement dummy AI planning service",
              "Test backend response shape",
            ],
          },
          {
            id: 2,
            title: "Day 2 – Frontend scaffold & UI",
            due: "2025-12-09",
            tasks: [
              "Create Next.js + Tailwind scaffold",
              "Connect frontend /plan endpoint",
              "Render milestones & tasks dashboard",
            ],
          },
        ],
      });
      setSource("fallback");
    }
  }, []);

  if (!plan) {
    return <p className="text-sm text-slate-400">Loading plan…</p>;
  }

  return (
    <section className="space-y-4">
      <div className="flex items-start justify-between gap-2">
        <div>
          <h2 className="text-xl font-semibold mb-1">Your execution plan</h2>
          <p className="text-sm text-slate-400">
            Goal: <span className="text-slate-100">{plan.goal}</span>
          </p>
          {plan.deadline && (
            <p className="text-xs text-slate-500">
              Target deadline:{" "}
              <span className="text-slate-200">{plan.deadline}</span>
            </p>
          )}
        </div>

        {/* Tiny badge showing where the data came from */}
        <span
          className={`text-[10px] px-2 py-1 rounded-full border ${
            source === "backend"
              ? "bg-emerald-500/10 border-emerald-500/60 text-emerald-300"
              : "bg-slate-900 border-slate-600 text-slate-300"
          }`}
        >
          {source === "backend" ? "Live from backend" : "Using demo data"}
        </span>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {plan.milestones?.map((m) => (
          <article
            key={m.id}
            className="bg-slate-900/60 border border-slate-800 rounded-2xl p-4 space-y-2"
          >
            <div className="flex items-start justify-between gap-2">
              <h3 className="font-semibold text-sm md:text-base">
                {m.title}
              </h3>
              {m.due && (
                <span className="text-[10px] md:text-xs text-slate-400 bg-slate-950/60 border border-slate-800 rounded-full px-2 py-1">
                  Due: {m.due}
                </span>
              )}
            </div>
            <ul className="text-xs md:text-sm list-disc list-inside space-y-1 text-slate-300">
              {m.tasks?.map((t, idx) => (
                <li key={idx}>{t}</li>
              ))}
            </ul>
          </article>
        ))}
      </div>
    </section>
  );
}

"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { getStatus, StatusGoal } from "@/lib/api";

type Filter = "all" | "in_progress" | "completed";

export default function StatusPage() {
  const [goals, setGoals] = useState<StatusGoal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<Filter>("all");

  useEffect(() => {
    async function fetchStatus() {
      try {
        const data = await getStatus();
        setGoals(data.goals ?? []);
      } catch (err) {
        const message =
        err instanceof Error ? err.message : "Failed to load status";
        setError(message);
      } finally {
        setLoading(false);
      }
    }

    fetchStatus();
  }, []);

  const filteredGoals = useMemo(() => {
    if (filter === "all") return goals;
    return goals.filter((g) => g.status === filter);
  }, [goals, filter]);

  const summary = useMemo(() => {
    const totalGoals = goals.length;
    const totalTasks = goals.reduce((sum, g) => sum + g.tasks.length, 0);
    const completedTasks = goals.reduce(
      (sum, g) => sum + g.tasks.filter((t) => t.status === "completed").length,
      0
    );

    return { totalGoals, totalTasks, completedTasks };
  }, [goals]);

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-950 to-slate-900 text-slate-50 flex flex-col items-center px-4 py-10">
      <div className="w-full max-w-5xl space-y-8">
        {/* Top bar / nav */}
        <header className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold tracking-tight">
              TaskPilot — Dashboard
            </h1>
            <p className="mt-1 text-xs md:text-sm text-slate-300 max-w-xl">
              See all your goals and tasks in one place. Use filters to focus on
              what&apos;s in progress or done.
            </p>
          </div>

          <nav className="flex gap-2 text-xs">
            <Link
              href="/"
              className="px-3 py-1.5 rounded-full border border-slate-600 bg-slate-900/60 hover:bg-slate-800 transition-colors"
            >
              + Plan new goal
            </Link>
          </nav>
        </header>

        {/* Summary strip */}
        <section className="grid gap-3 md:grid-cols-3">
          <div className="bg-slate-900/70 border border-slate-700 rounded-2xl p-4 space-y-1">
            <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wide">
              Goals
            </p>
            <p className="text-2xl font-bold">{summary.totalGoals}</p>
            <p className="text-xs text-slate-400">Total goals created</p>
          </div>
          <div className="bg-slate-900/70 border border-slate-700 rounded-2xl p-4 space-y-1">
            <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wide">
              Tasks
            </p>
            <p className="text-2xl font-bold">{summary.totalTasks}</p>
            <p className="text-xs text-slate-400">All tasks across goals</p>
          </div>
          <div className="bg-slate-900/70 border border-slate-700 rounded-2xl p-4 space-y-1">
            <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wide">
              Completed
            </p>
            <p className="text-2xl font-bold">
              {summary.completedTasks}/{summary.totalTasks || 0}
            </p>
            <p className="text-xs text-slate-400">Tasks marked completed</p>
          </div>
        </section>

        {/* Filters */}
        <section className="flex flex-wrap items-center justify-between gap-3">
          <h2 className="text-sm font-semibold text-slate-200">
            Goals overview
          </h2>
          <div className="inline-flex rounded-full border border-slate-700 bg-slate-900/60 p-1 text-xs">
            <button
              type="button"
              onClick={() => setFilter("all")}
              className={`px-3 py-1 rounded-full ${
                filter === "all"
                  ? "bg-slate-100 text-slate-900"
                  : "text-slate-300 hover:bg-slate-800"
              }`}
            >
              All
            </button>
            <button
              type="button"
              onClick={() => setFilter("in_progress")}
              className={`px-3 py-1 rounded-full ${
                filter === "in_progress"
                  ? "bg-blue-500 text-white"
                  : "text-slate-300 hover:bg-slate-800"
              }`}
            >
              In progress
            </button>
            <button
              type="button"
              onClick={() => setFilter("completed")}
              className={`px-3 py-1 rounded-full ${
                filter === "completed"
                  ? "bg-emerald-500 text-white"
                  : "text-slate-300 hover:bg-slate-800"
              }`}
            >
              Completed
            </button>
          </div>
        </section>

        {/* Main content */}
        <section className="bg-slate-900/70 border border-slate-700 rounded-2xl shadow-xl p-5 min-h-[200px]">
          {loading && (
            <div className="space-y-3">
              <div className="h-4 w-32 bg-slate-800/80 rounded animate-pulse" />
              <div className="grid gap-3 md:grid-cols-2">
                {[1, 2, 3, 4].map((i) => (
                  <div
                    key={i}
                    className="h-32 bg-slate-900 border border-slate-800 rounded-2xl animate-pulse"
                  />
                ))}
              </div>
            </div>
          )}

          {!loading && error && (
            <p className="text-sm text-red-400">{error}</p>
          )}

          {!loading && !error && filteredGoals.length === 0 && (
            <div className="text-sm text-slate-300 space-y-1">
              <p>No goals match this filter.</p>
              <p>
                Try switching filters above or{" "}
                <Link href="/" className="text-blue-400 underline">
                  create a new plan.
                </Link>
              </p>
            </div>
          )}

          {!loading && !error && filteredGoals.length > 0 && (
            <div className="grid gap-4 md:grid-cols-2">
              {filteredGoals.map((goal) => {
                const totalTasks = goal.tasks.length;
                const completedTasks = goal.tasks.filter(
                  (t) => t.status === "completed"
                ).length;
                const percent =
                  totalTasks === 0
                    ? 0
                    : Math.round((completedTasks / totalTasks) * 100);

                return (
                  <article
                    key={goal.id}
                    className="bg-slate-950/80 border border-slate-700 rounded-2xl p-4 space-y-3 shadow-md"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="space-y-1">
                        <h3 className="text-base font-semibold text-slate-50">
                          Goal #{goal.id}
                        </h3>
                        <p className="text-sm text-slate-200">
                          {goal.goal}
                        </p>
                      </div>

                      <span
                        className={`inline-flex items-center justify-center text-[10px] uppercase tracking-wide px-2 py-0.5 rounded-full border ${
                          goal.status === "in_progress"
                            ? "bg-blue-500/10 text-blue-300 border-blue-500/40"
                            : goal.status === "completed"
                            ? "bg-emerald-500/10 text-emerald-300 border-emerald-500/40"
                            : "bg-slate-700/40 text-slate-200 border-slate-500/40"
                        }`}
                      >
                        {goal.status}
                      </span>
                    </div>

                    {/* Progress bar */}
                    <div className="space-y-1">
                      <div className="flex items-center justify-between text-[11px] text-slate-400">
                        <span>
                          {completedTasks}/{totalTasks || 0} tasks completed
                        </span>
                        <span>{percent}%</span>
                      </div>
                      <div className="h-1.5 w-full rounded-full bg-slate-800 overflow-hidden">
                        <div
                          className="h-full rounded-full bg-blue-500 transition-all"
                          style={{ width: `${percent}%` }}
                        />
                      </div>
                    </div>

                    {/* Task list preview */}
                    <div className="space-y-1.5">
                      <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wide">
                        Tasks
                      </p>
                      {goal.tasks.length === 0 ? (
                        <p className="text-xs text-slate-400">
                          No tasks recorded for this goal yet.
                        </p>
                      ) : (
                        <ul className="space-y-1.5 text-xs text-slate-100 max-h-32 overflow-auto pr-1">
                          {goal.tasks.map((t) => (
                            <li key={t.id} className="flex items-start gap-2">
                              <span className="mt-[3px] h-1.5 w-1.5 rounded-full bg-blue-400" />
                              <span>
                                <span className="mr-1 text-[11px] px-1 py-[1px] rounded-full bg-slate-800 border border-slate-600 text-slate-300">
                                  {t.status}
                                </span>
                                {t.title}
                              </span>
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  </article>
                );
              })}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}

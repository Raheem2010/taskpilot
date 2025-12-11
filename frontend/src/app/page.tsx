"use client";

import { useState } from "react";
import Link from "next/link";
import { createPlan, PlanResponse } from "../lib/api";

export default function HomePage() {
  const [goal, setGoal] = useState("");
  const [loading, setLoading] = useState(false);
  const [plan, setPlan] = useState<PlanResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPlan(null);

    try {
      const response = await createPlan(goal);
      setPlan(response);
    } catch (err) {
      const message =
      err instanceof Error ? err.message : "Failed to load status";
      setError(message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-950 to-slate-900 text-slate-50 flex flex-col items-center px-4 py-10">
      <div className="w-full max-w-3xl space-y-8">
        {/* Hero / Header */}
        <header className="text-center space-y-3">
          <h1 className="text-4xl font-extrabold tracking-tight">
            TaskPilot
          </h1>
          <p className="text-sm text-slate-300 max-w-xl mx-auto">
            Turn a big, fuzzy goal into a clear plan with milestones and actionable tasks.
          </p>

          <div className="flex justify-center">
            <Link
              href="/status"
              className="mt-2 inline-flex items-center px-3 py-1.5 text-xs rounded-full border border-slate-600 bg-slate-900/60 hover:bg-slate-800 transition-colors"
            >
              View all goals
            </Link>
          </div>
        </header>

        {/* Form Card */}
        <section className="bg-slate-900/70 border border-slate-700 rounded-2xl shadow-xl p-5 space-y-4">
          <h2 className="text-lg font-semibold text-slate-100 text-left">
            1. Describe your goal
          </h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <textarea
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              placeholder="e.g. Launch my shoe brand in 3 months with online sales and social media presence"
              className="w-full p-3 mt-1 border border-slate-600 rounded-xl text-sm text-black bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={4}
              required
            />

            <button
              type="submit"
              disabled={!goal.trim() || loading}
              className="inline-flex items-center justify-center w-full md:w-auto px-5 py-2.5 rounded-xl bg-blue-500 hover:bg-blue-600 disabled:bg-slate-600 text-sm font-medium text-white transition-colors"
            >
              {loading ? "Generating plan..." : "Generate Plan"}
            </button>
          </form>

          {error && (
            <p className="mt-2 text-sm text-red-400">
              {error}
            </p>
          )}
        </section>

        {/* Plan Result */}
        {plan && (
          <section className="space-y-4">
            <div className="space-y-1">
              <h2 className="text-xl font-semibold text-slate-50">
                2. Your plan
              </h2>
              <p className="text-sm text-slate-300">
                Goal:&nbsp;
                <span className="font-medium text-slate-100">
                  {plan.goal}
                </span>
              </p>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              {plan.milestones.map((m, idx) => (
                <article
                  key={idx}
                  className="bg-slate-900/60 border border-slate-700 rounded-2xl shadow-md p-4 flex flex-col gap-2"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="space-y-1">
                      <h3 className="text-base font-semibold text-slate-50">
                        Milestone {idx + 1}
                      </h3>
                      <p className="text-sm font-medium text-blue-300">
                        {m.title}
                      </p>
                    </div>
                    <span className="inline-flex items-center justify-center text-[11px] uppercase tracking-wide px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-300 border border-blue-500/30">
                      Step {idx + 1}
                    </span>
                  </div>

                  {m.description && (
                    <p className="text-xs text-slate-300 leading-relaxed">
                      {m.description}
                    </p>
                  )}

                  <div className="mt-2 space-y-1.5">
                    <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wide">
                      Tasks
                    </p>
                    <ul className="space-y-1.5 text-xs text-slate-100">
                      {m.tasks.map((t) => (
                        <li
                          key={t.id}
                          className="flex items-start gap-2"
                        >
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
                  </div>
                </article>
              ))}
            </div>
          </section>
        )}
      </div>
    </main>
  );
}

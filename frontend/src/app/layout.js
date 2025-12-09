import "./globals.css";
export const metadata = {
  title: "TaskPilot",
  description: "Agentic workflow planner for AI Agents Assemble",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-950 text-slate-100">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <header className="flex items-center justify-between mb-8">
            <h1 className="text-2xl font-bold">
              TaskPilot<span className="text-indigo-400">.ai</span>
            </h1>
            <span className="text-xs text-slate-400">
              AI Agents Assemble Hackathon
            </span>
          </header>

          <main>{children}</main>
        </div>
      </body>
    </html>
  );
}

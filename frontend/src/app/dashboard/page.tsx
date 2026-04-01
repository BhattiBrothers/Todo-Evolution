"use client"
// [Spec: SPEC-001 — Task CRUD, SPEC-002 — Authentication]
// Dashboard — task management via Next.js proxy to FastAPI

import { useState, useEffect, useCallback } from "react"
import { useRouter } from "next/navigation"
import { authClient } from "@/lib/auth-client"

interface Task {
  id: number
  title: string
  description: string | null
  completed: boolean
  created_at: string
  updated_at: string
}

export default function DashboardPage() {
  const router = useRouter()
  const { data: session, isPending } = authClient.useSession()
  const [tasks, setTasks] = useState<Task[]>([])
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [loading, setLoading] = useState(true)
  const [adding, setAdding] = useState(false)
  const [error, setError] = useState("")

  useEffect(() => {
    if (!isPending && !session) {
      router.push("/login")
    }
  }, [isPending, session, router])

  const fetchTasks = useCallback(async () => {
    if (!session?.user?.id) return
    setLoading(true)
    try {
      const res = await fetch(`/api/tasks`)
      if (!res.ok) throw new Error("Failed to fetch tasks")
      setTasks(await res.json())
    } catch {
      setError("Could not load tasks")
    } finally {
      setLoading(false)
    }
  }, [session])

  useEffect(() => {
    if (session) fetchTasks()
  }, [session, fetchTasks])

  async function addTask(e: React.FormEvent) {
    e.preventDefault()
    if (!title.trim()) return
    setAdding(true)
    const res = await fetch(`/api/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: title.trim(), description: description.trim() }),
    })
    setAdding(false)
    if (res.ok) {
      setTitle("")
      setDescription("")
      fetchTasks()
    }
  }

  async function toggleComplete(taskId: number) {
    await fetch(`/api/tasks/${taskId}/complete`, { method: "PATCH" })
    fetchTasks()
  }

  async function deleteTask(taskId: number) {
    await fetch(`/api/tasks/${taskId}`, { method: "DELETE" })
    fetchTasks()
  }

  async function handleSignOut() {
    await authClient.signOut()
    router.push("/login")
  }

  if (isPending || !session) {
    return <div className="min-h-screen flex items-center justify-center text-zinc-500">Loading…</div>
  }

  return (
    <div className="min-h-screen bg-zinc-50">
      <header className="bg-white border-b border-zinc-200 px-6 py-4 flex items-center justify-between">
        <h1 className="text-xl font-bold text-zinc-900">Todo Evolution</h1>
        <div className="flex items-center gap-4">
          <span className="text-sm text-zinc-600">{session.user.email}</span>
          <button
            onClick={handleSignOut}
            className="text-sm text-zinc-500 hover:text-zinc-900 underline"
          >
            Sign out
          </button>
        </div>
      </header>

      <main className="max-w-2xl mx-auto px-6 py-8 space-y-6">
        <form onSubmit={addTask} className="bg-white rounded-2xl shadow p-6 space-y-3">
          <h2 className="text-base font-semibold text-zinc-900">New Task</h2>
          <input
            type="text"
            placeholder="Task title"
            required
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full border border-zinc-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-zinc-900"
          />
          <input
            type="text"
            placeholder="Description (optional)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full border border-zinc-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-zinc-900"
          />
          <button
            type="submit"
            disabled={adding}
            className="bg-zinc-900 text-white rounded-lg px-4 py-2 text-sm font-medium hover:bg-zinc-700 disabled:opacity-50"
          >
            {adding ? "Adding…" : "Add Task"}
          </button>
        </form>

        <div className="space-y-3">
          {error && <p className="text-red-600 text-sm">{error}</p>}
          {loading ? (
            <p className="text-zinc-500 text-sm">Loading tasks…</p>
          ) : tasks.length === 0 ? (
            <p className="text-zinc-500 text-sm">No tasks yet. Add one above!</p>
          ) : (
            tasks.map((task) => (
              <div key={task.id} className="bg-white rounded-2xl shadow px-5 py-4 flex items-start gap-4">
                <button
                  onClick={() => toggleComplete(task.id)}
                  className={`mt-0.5 h-5 w-5 rounded-full border-2 flex-shrink-0 transition-colors ${
                    task.completed ? "bg-zinc-900 border-zinc-900" : "border-zinc-300 hover:border-zinc-600"
                  }`}
                />
                <div className="flex-1 min-w-0">
                  <p className={`text-sm font-medium ${task.completed ? "line-through text-zinc-400" : "text-zinc-900"}`}>
                    {task.title}
                  </p>
                  {task.description && (
                    <p className="text-xs text-zinc-500 mt-0.5">{task.description}</p>
                  )}
                </div>
                <button
                  onClick={() => deleteTask(task.id)}
                  className="text-zinc-400 hover:text-red-500 text-xs flex-shrink-0"
                >
                  Delete
                </button>
              </div>
            ))
          )}
        </div>
      </main>
    </div>
  )
}

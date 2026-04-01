"use client"
// [Spec: SPEC-001 — Task CRUD, SPEC-002 — Auth, Phase III — AI Chat]
// Dashboard — task management + AI chat assistant

import { useState, useEffect, useCallback, useRef } from "react"
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

interface ChatMessage {
  role: "user" | "assistant"
  content: string
}

export default function DashboardPage() {
  const router = useRouter()
  const { data: session, isPending } = authClient.useSession()

  // Tasks state
  const [tasks, setTasks] = useState<Task[]>([])
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [loading, setLoading] = useState(true)
  const [adding, setAdding] = useState(false)
  const [taskError, setTaskError] = useState("")

  // Chat state
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([])
  const [chatInput, setChatInput] = useState("")
  const [chatLoading, setChatLoading] = useState(false)
  const chatEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!isPending && !session) router.push("/login")
  }, [isPending, session, router])

  const fetchTasks = useCallback(async () => {
    if (!session?.user?.id) return
    setLoading(true)
    try {
      const res = await fetch(`/api/tasks`)
      if (!res.ok) throw new Error()
      setTasks(await res.json())
    } catch {
      setTaskError("Could not load tasks")
    } finally {
      setLoading(false)
    }
  }, [session])

  useEffect(() => {
    if (session) fetchTasks()
  }, [session, fetchTasks])

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [chatHistory])

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

  async function sendChat(e: React.FormEvent) {
    e.preventDefault()
    if (!chatInput.trim() || chatLoading) return
    const userMsg: ChatMessage = { role: "user", content: chatInput.trim() }
    setChatHistory((prev) => [...prev, userMsg])
    setChatInput("")
    setChatLoading(true)

    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: userMsg.content,
        history: chatHistory.map((m) => ({ role: m.role, content: m.content })),
      }),
    })
    setChatLoading(false)
    if (res.ok) {
      const { reply } = await res.json()
      setChatHistory((prev) => [...prev, { role: "assistant", content: reply }])
      fetchTasks() // Refresh tasks if AI modified them
    }
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
      {/* Header */}
      <header className="bg-white border-b border-zinc-200 px-6 py-4 flex items-center justify-between">
        <h1 className="text-xl font-bold text-zinc-900">Todo Evolution</h1>
        <div className="flex items-center gap-4">
          <span className="text-sm text-zinc-600">{session.user.email}</span>
          <button onClick={handleSignOut} className="text-sm text-zinc-500 hover:text-zinc-900 underline">
            Sign out
          </button>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* LEFT — Tasks */}
        <div className="space-y-4">
          <form onSubmit={addTask} className="bg-white rounded-2xl shadow p-5 space-y-3">
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

          <div className="space-y-2">
            {taskError && <p className="text-red-600 text-sm">{taskError}</p>}
            {loading ? (
              <p className="text-zinc-500 text-sm">Loading tasks…</p>
            ) : tasks.length === 0 ? (
              <p className="text-zinc-500 text-sm">No tasks yet.</p>
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
                  <button onClick={() => deleteTask(task.id)} className="text-zinc-400 hover:text-red-500 text-xs">
                    Delete
                  </button>
                </div>
              ))
            )}
          </div>
        </div>

        {/* RIGHT — AI Chat */}
        <div className="bg-white rounded-2xl shadow flex flex-col h-[600px]">
          <div className="px-5 py-4 border-b border-zinc-100">
            <h2 className="text-base font-semibold text-zinc-900">AI Assistant</h2>
            <p className="text-xs text-zinc-500">Ask me to list, add, complete or delete tasks</p>
          </div>

          <div className="flex-1 overflow-y-auto px-5 py-4 space-y-3">
            {chatHistory.length === 0 && (
              <p className="text-zinc-400 text-sm">Say hello! Try: "Show my tasks" or "Add a task: Call dentist"</p>
            )}
            {chatHistory.map((msg, i) => (
              <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-2 text-sm whitespace-pre-wrap ${
                    msg.role === "user"
                      ? "bg-zinc-900 text-white rounded-br-sm"
                      : "bg-zinc-100 text-zinc-900 rounded-bl-sm"
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            ))}
            {chatLoading && (
              <div className="flex justify-start">
                <div className="bg-zinc-100 rounded-2xl rounded-bl-sm px-4 py-2 text-sm text-zinc-500">
                  Thinking…
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          <form onSubmit={sendChat} className="px-5 py-4 border-t border-zinc-100 flex gap-2">
            <input
              type="text"
              placeholder="Ask your AI assistant…"
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              className="flex-1 border border-zinc-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-zinc-900"
            />
            <button
              type="submit"
              disabled={chatLoading}
              className="bg-zinc-900 text-white rounded-lg px-4 py-2 text-sm font-medium hover:bg-zinc-700 disabled:opacity-50"
            >
              Send
            </button>
          </form>
        </div>
      </main>
    </div>
  )
}

// [Spec: SPEC-001 — Task CRUD]
// Next.js proxy: PATCH/DELETE /api/tasks/[taskId] → FastAPI

import { NextRequest, NextResponse } from "next/server"
import { headers } from "next/headers"
import { auth } from "@/lib/auth"
import { SignJWT } from "jose"

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
const SECRET = new TextEncoder().encode(process.env.BETTER_AUTH_SECRET)

async function makeToken(userId: string): Promise<string> {
  return new SignJWT({ sub: userId })
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt()
    .setExpirationTime("1h")
    .sign(SECRET)
}

export async function PATCH(
  req: NextRequest,
  { params }: { params: Promise<{ taskId: string }> }
) {
  const session = await auth.api.getSession({ headers: await headers() })
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
  const { taskId } = await params
  const token = await makeToken(session.user.id)
  const res = await fetch(`${API}/api/${session.user.id}/tasks/${taskId}/complete`, {
    method: "PATCH",
    headers: { Authorization: `Bearer ${token}` },
  })
  return NextResponse.json(await res.json(), { status: res.status })
}

export async function DELETE(
  req: NextRequest,
  { params }: { params: Promise<{ taskId: string }> }
) {
  const session = await auth.api.getSession({ headers: await headers() })
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
  const { taskId } = await params
  const token = await makeToken(session.user.id)
  const res = await fetch(`${API}/api/${session.user.id}/tasks/${taskId}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  })
  return new NextResponse(null, { status: 204 })
}

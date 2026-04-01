// [Spec: Phase III — AI Chatbot]
// Next.js proxy: POST /api/chat → FastAPI chat endpoint

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

export async function POST(req: NextRequest) {
  const session = await auth.api.getSession({ headers: await headers() })
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
  const token = await makeToken(session.user.id)
  const body = await req.json()
  const res = await fetch(`${API}/api/${session.user.id}/chat`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return NextResponse.json(await res.json(), { status: res.status })
}

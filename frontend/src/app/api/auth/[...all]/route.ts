// [Spec: SPEC-002 — Authentication]
// Better Auth catch-all API route handler

import { auth } from "@/lib/auth"
import { toNextJsHandler } from "better-auth/next-js"

export const { GET, POST } = toNextJsHandler(auth)

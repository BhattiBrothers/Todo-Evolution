# Feature Spec: Authentication
## Phase II — Full-Stack Web Application

**Spec ID:** SPEC-002  
**Phase:** II  
**Status:** Approved

---

## User Stories

- As a visitor, I can sign up with email and password
- As a user, I can sign in with my email and password
- As a user, I can sign out
- As a user, my tasks are private and only visible to me

---

## Acceptance Criteria

### Sign Up
- Email (required, valid format), Password (required, min 8 chars), Name (required)
- Duplicate email shows error: "An account with this email already exists"
- On success: redirect to dashboard

### Sign In
- Email + password required
- Wrong credentials: "Invalid email or password"
- On success: redirect to dashboard, JWT token issued

### Sign Out
- Clears session, redirects to login page

### Authorization
- All /api/* endpoints require valid JWT token
- No token → 401 Unauthorized
- Each user sees only their own tasks

---

## Tech
- Better Auth (Next.js frontend)
- JWT tokens shared with FastAPI backend via BETTER_AUTH_SECRET

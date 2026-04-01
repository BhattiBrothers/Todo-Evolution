# Database Schema — Phase II

**Spec ID:** SPEC-003  
**Phase:** II

---

## Tables

### users (managed by Better Auth)
- id: string (primary key)
- email: string (unique)
- name: string
- created_at: timestamp

### tasks
- id: integer (primary key, auto-increment)
- user_id: string (foreign key → users.id)
- title: string (not null, max 200)
- description: text (nullable, max 1000)
- completed: boolean (default false)
- created_at: timestamp
- updated_at: timestamp

## Indexes
- tasks.user_id (filter by user)
- tasks.completed (filter by status)

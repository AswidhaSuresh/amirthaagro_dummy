-- ===============================
-- 📦 Users Table
-- ===============================
create table if not exists users (
    id uuid primary key default gen_random_uuid(),
    email text not null unique,
    role text not null check (role in ('admin', 'client')),
    is_active boolean default true,
    created_at timestamp default now()
);

-- ===============================
-- 🧾 Clients Table
-- ===============================
create table if not exists clients (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references users(id) on delete cascade,
    party_id text not null unique,
    password_set boolean default false,
    mobile_number text,
    created_at timestamp default now()
);

-- ===============================
-- 🔐 Password Resets Table
-- ===============================
create table if not exists password_resets (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references users(id) on delete cascade,
    token text not null,
    expires_at timestamp not null,
    used boolean default false,
    created_at timestamp default now()
);

-- ===============================
-- 📊 Product Data Table
-- ===============================
create table if not exists stocks_data (
    id uuid primary key default gen_random_uuid(),
    party_id text not null references clients(party_id) on delete cascade,
    uploaded_by uuid references users(id) on delete set null,
    data jsonb not null,
    uploaded_at timestamp default now()
);

-- ===============================
-- 📌 Optional Tables (Remind Later)
-- ===============================
-- Uncomment if needed after core setup

-- -- Activity Logs Table
-- create table if not exists activity_logs (
--     id uuid primary key default gen_random_uuid(),
--     user_id uuid references users(id) on delete cascade,
--     action text not null,
--     details jsonb,
--     created_at timestamp default now()
-- );

-- -- Admin Notes Table
-- create table if not exists admin_notes (
--     id uuid primary key default gen_random_uuid(),
--     client_id uuid references clients(id) on delete cascade,
--     note text not null,
--     created_at timestamp default now()
-- );

-- -- Support Requests Table
-- create table if not exists support_requests (
--     id uuid primary key default gen_random_uuid(),
--     client_id uuid references clients(id) on delete cascade,
--     type text check (type in ('password_reset', 'feedback')),
--     message text,
--     status text default 'open',
--     created_at timestamp default now()
-- );

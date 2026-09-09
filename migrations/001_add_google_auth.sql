-- Migration: Add Google OAuth and enhanced user fields
-- Compatible with PostgreSQL 12+

-- 1. Add email column (nullable for backward compatibility with existing accounts)
ALTER TABLE users ADD COLUMN IF NOT EXISTS email VARCHAR(120);

-- 2. Add google_id column for storing Google OAuth unique subject identifier
ALTER TABLE users ADD COLUMN IF NOT EXISTS google_id VARCHAR(100);

-- 3. Add auth_provider column to track authentication method ('local', 'google', 'both')
ALTER TABLE users ADD COLUMN IF NOT EXISTS auth_provider VARCHAR(20) DEFAULT 'local';

-- 4. Allow nullable passwords (for users authenticating solely via Google OAuth)
ALTER TABLE users ALTER COLUMN password DROP NOT NULL;

-- 5. Add unique indexes if they don't already exist
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email) WHERE email IS NOT NULL;
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_google_id ON users(google_id) WHERE google_id IS NOT NULL;

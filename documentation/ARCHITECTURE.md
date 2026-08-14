# Architecture

This document explains how the FastAPI_Auth application is structured and how data flows through it.

## Layered Architecture

The backend follows a simple layered pattern. Each layer has a single responsibility.

```
HTTP Request
     │
     ▼
 ┌─────────────┐
 │   Routes     │  ← Receives requests, validates input, returns responses
 └──────┬──────┘
        │
        ▼
 ┌─────────────┐
 │    Auth      │  ← Verifies JWT tokens, fetches current user
 └──────┬──────┘
        │
        ▼
 ┌─────────────┐
 │  Schemas     │  ← Validates and serializes data (Pydantic)
 └──────┬──────┘
        │
        ▼
 ┌─────────────┐
 │   Models     │  ← Defines database table structure (SQLAlchemy)
 └──────┬──────┘
        │
        ▼
 ┌─────────────┐
 │  Database    │  ← Manages DB connections and sessions
 └──────┬──────┘
        │
        ▼
 ┌─────────────┐
 │   Alembic    │  ← Manages schema migrations (version control for DB)
 └─────────────┘
```

## Component Breakdown

### main.py
The application entry point. It creates the FastAPI app instance and includes the API router. Database schema changes are managed by Alembic migrations, not auto-created on startup.

### backend/alembic/
Alembic migration tooling:
- `env.py` — configures the migration environment and connects to your database
- `script.py.mako` — template for generating new migration files
- `versions/` — stores all generated migration scripts

### app/routes.py
Defines all HTTP endpoints. Each route function receives validated data from Pydantic schemas and returns JSON responses.

### app/auth.py
Provides reusable "dependencies" for FastAPI. The `get_current_user` function extracts a JWT from the request, decodes it, and returns the authenticated user. FastAPI automatically runs this before any route that needs it.

### app/security.py
Handles all cryptographic operations:
- `get_password_hash()` — converts a plain-text password into a bcrypt hash
- `create_access_token()` — encodes user data into a signed JWT with an expiration time

### app/schemas.py
Pydantic models that define what data looks like when it enters or leaves the API. They automatically validate types and formats (e.g., email format, minimum password length).

### app/db_models.py
SQLAlchemy ORM models. Each class maps to a database table. The `User` class defines the `users` table schema.

### app/database.py
Creates the SQLAlchemy engine and session factory. The `get_db()` function provides a database session to route handlers and ensures it is closed afterward. Also exports `Base` which Alembic uses to detect model changes.

## Data Flow Examples

### User Registration

```
Client → POST /register/ (JSON body)
       ↓
routes.py: receives UserIn schema
       ↓
auth.py: checks if username/email already exists
       ↓
security.py: hashes the password
       ↓
db_models.py: creates User ORM object
       ↓
database.py: saves to MySQL
       ↓
Client ← User JSON response
```

### User Login

```
Client → POST /token (form data: username + password)
       ↓
routes.py: receives OAuth2PasswordRequestForm
       ↓
auth.py: fetches user from database
       ↓
security.py: verifies password hash
       ↓
security.py: creates JWT access token
       ↓
Client ← { access_token, token_type: "bearer" }
```

### Accessing a Protected Endpoint

```
Client → GET /conversation/ (Header: Authorization: Bearer <token>)
       ↓
auth.py: extracts token from header
       ↓
security.py: decodes and validates JWT
       ↓
auth.py: fetches user from database
       ↓
routes.py: returns secure conversation data
       ↓
Client ← { conversation: "...", current_user: "john_doe" }
```

## Key Concepts for Beginners

### What is a schema?
A schema is a "contract" for data. It says: "If you send me a user, it must have an email, a username, and a password that is at least 8 characters long." FastAPI uses schemas to automatically validate incoming requests.

### What is a model?
A model is a Python class that maps to a database table. SQLAlchemy uses models to let you work with database rows as if they were Python objects.

### What is a dependency?
FastAPI dependencies are reusable functions that run before your route code. `get_db` gives every route a database session. `get_current_user` checks the JWT and gives every protected route the logged-in user.

### What is the session?
A database session is a temporary workspace for talking to the database. It tracks changes you make so they can be saved (committed) or discarded.

### What is Alembic?
Alembic is a migration tool for SQLAlchemy. Think of it like "version control for your database schema." When you change a model (add a column, change a type), Alembic generates a migration script that updates the actual database to match your code. This prevents data loss and keeps your database in sync with your application.

# FastAPI_Auth

A backend authentication service built with **FastAPI**, **SQLAlchemy**, and **MySQL**. It provides user registration, OAuth2 password login, and protected API endpoints using JWT bearer tokens.

## Features

- User registration with duplicate email/username checks
- Secure password hashing with bcrypt
- JWT-based authentication (OAuth2 password flow)
- Protected API endpoints
- Auto-generated API docs with Swagger UI

## Tech Stack

| Tool | Purpose |
|------|---------|
| **FastAPI** | Modern Python web framework |
| **SQLAlchemy 2.x** | ORM for database operations |
| **MySQL** | Relational database |
| **python-jose** | JWT encoding and decoding |
| **passlib + bcrypt** | Password hashing |
| **python-dotenv** | Environment variable management |
| **Pydantic** | Data validation and serialization |
| **Alembic** | Database schema migration tool |

## Prerequisites

- Python 3.8 or higher
- MySQL Server running locally
- `uv` or `pip` for dependency management

## Project Structure

```
FastAPI_Auth/
├── .env                        # Environment variables (DB URL, secret key)
├── backend/
│   ├── main.py                 # FastAPI app entry point
│   ├── pyproject.toml          # Dependencies and project metadata
│   ├── alembic.ini             # Alembic configuration
│   ├── alembic/                # Migration scripts and environment
│   │   ├── env.py              # Migration environment config
│   │   ├── script.py.mako      # Migration file template
│   │   └── versions/           # Generated migration files
│   └── app/
│       ├── __init__.py         # Makes 'app' a Python package
│       ├── database.py         # DB engine, session, and connection setup
│       ├── db_models.py        # SQLAlchemy ORM models
│       ├── schemas.py          # Pydantic request/response schemas
│       ├── security.py         # JWT creation and password hashing
│       ├── auth.py             # Authentication dependencies
│       └── routes.py           # API route definitions
└── documentation/
    ├── ARCHITECTURE.md         # System architecture and data flow
    ├── API_REFERENCE.md        # Detailed endpoint documentation
    └── MIGRATIONS.md           # Alembic migration guide
```

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/FastAPI_Auth.git
cd FastAPI_Auth
```

### 2. Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/Fastapi_Auth
```

> **Important:** Generate a strong `SECRET_KEY` for production. You can generate one with:
> ```bash
> python -c "import secrets; print(secrets.token_urlsafe(32))"
> ```

### 5. Set up database migrations (Alembic)

This project uses Alembic to manage database schema changes. Run these commands from the `backend/` directory:

```bash
cd backend

# Generate the first migration from your models
alembic revision --autogenerate -m "Initial migration"

# Apply the migration to your database
alembic upgrade head
```

### 6. Create the database

```sql
CREATE DATABASE Fastapi_Auth;
```

> **Note:** Make sure the database exists before running Alembic migrations.

### 7. Run the server

```bash
cd backend
uvicorn main:app --reload
```

The API will be available at: **http://127.0.0.1:8000**

## Using the API

### Interactive Docs (Swagger UI)

Open **http://127.0.0.1:8000/docs** in your browser. This is the easiest way to test endpoints without writing code.

### Example Requests

#### Register a new user

```bash
curl -X POST "http://127.0.0.1:8000/register/" \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "email": "john@example.com", "password": "securepass123"}'
```

#### Login and get a token

```bash
curl -X POST "http://127.0.0.1:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=securepass123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Access a protected endpoint

```bash
curl -X GET "http://127.0.0.1:8000/conversation/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Authentication Flow

This project uses **OAuth2 password flow** with **JWT tokens**:

1. Client sends username and password to `/token`
2. Server validates credentials and returns a JWT
3. Client includes the JWT in the `Authorization: Bearer <token>` header
4. Server validates the token on each protected request

## Database Migrations

This project uses **Alembic** to manage database schema changes. When you modify a model in `db_models.py`, you must generate and apply a migration.

### Typical workflow

1. Edit a model in `backend/app/db_models.py` (e.g., add a column)
2. Generate a migration script:
   ```bash
   cd backend
   alembic revision --autogenerate -m "Describe your change"
   ```
3. Apply the migration:
   ```bash
   alembic upgrade head
   ```

### Useful commands

| Command | Purpose |
|---------|---------|
| `alembic revision --autogenerate -m "msg"` | Create a new migration script |
| `alembic upgrade head` | Apply all pending migrations |
| `alembic downgrade -1` | Roll back the last migration |
| `alembic current` | Show current migration version |
| `alembic history` | Show migration history |

## Security Notes

- Never commit `.env` to version control
- Always use a strong, random `SECRET_KEY` in production
- Passwords are hashed with bcrypt — never stored in plain text
- JWT tokens expire after 15 minutes (configurable in `security.py`)

## License

MIT

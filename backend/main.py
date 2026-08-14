"""
backend/main.py

Entry point for the FastAPI_Auth application.
Creates the FastAPI app, includes the API router, and starts the server.

Database schema changes are managed by Alembic migrations.
Run 'alembic upgrade head' to create or update the database schema.
"""
from fastapi import FastAPI
import uvicorn
from app import db_models
from app.database import engine
from app.routes import router

app = FastAPI()

# Database tables are now managed by Alembic migrations.
# Run 'alembic upgrade head' to create or update the schema.
# db_models.Base.metadata.create_all(bind=engine)

# Include all API routes
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
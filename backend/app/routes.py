"""
backend/app/routes.py

API route definitions.
Contains all HTTP endpoints: registration, login, and a protected conversation route.
"""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import auth, schemas, security
from app import db_models as models
from app.database import get_db

router = APIRouter()


@router.post("/register/", response_model=schemas.UserInDBBase)
async def register(user_in: schemas.UserIn, db: Session = Depends(get_db)):
    """Register a new user account.

    Validates that the username and email are unique,
    hashes the password, and saves the user to the database.

    Args:
        user_in: Validated registration data (username, email, password).
        db: Database session provided by FastAPI dependency injection.

    Returns:
        The created user object (without the password).

    Raises:
        HTTPException: 400 if username or email already exists.
    """
    db_user = auth.get_user(db, username=user_in.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password before storing it
    hashed_password = security.get_password_hash(user_in.password)
    db_user = models.User(**user_in.model_dump(exclude={"password"}), hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """OAuth2 compatible login endpoint.

    Accepts form-encoded username and password, verifies them,
    and returns a JWT access token.

    Args:
        form_data: OAuth2 password form data (username and password).
        db: Database session.

    Returns:
        A dictionary containing the access token and token type.

    Raises:
        HTTPException: 401 if username or password is incorrect.
    """
    user = auth.get_user(db, username=form_data.username)
    if not user or not security.pwd_context.verify(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/conversation/")
async def read_conversation(
    current_user: schemas.UserInDB = Depends(auth.get_current_user),
):
    """A protected endpoint that returns a secure conversation.

    Requires a valid JWT token in the Authorization header.

    Args:
        current_user: The authenticated user, injected by get_current_user dependency.

    Returns:
        A dictionary with the conversation message and the current username.
    """
    return {
        "conversation": "This is a secure conversation!",
        "current_user": current_user.username,
    }
from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal, Base, engine
from schemas import Create_User
from sqlalchemy.orm import Session
from db_model import User 
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/")
def create_user(user: Create_User, db: Session = Depends(get_db)):
    db_user = User(
        id=user.id,
        name=user.name,
        email=user.email,
        hashed_password=user.hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
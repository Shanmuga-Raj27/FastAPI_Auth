from pydantic import BaseModel, email_validator, password_validator

class Create_User(BaseModel):
    id: int
    name: str
    email: email_validator.EmailStr
    hashed_password: password_validator.PasswordStr

    class Config:
        from_attributes = True
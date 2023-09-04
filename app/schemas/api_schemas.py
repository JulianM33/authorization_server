from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    username: str = Field(default=None)
    email: str = Field(default=None)
    password: str = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "username": "John Smith",
                "email": "John@mail.com",
                "password": "password123",
            }
        }


class UserLoginSchema(BaseModel):
    email: str = Field(default=None)
    password: str = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "email": "john@mail.com",
                "password": "password123",
            }
        }

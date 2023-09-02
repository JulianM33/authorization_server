from typing import Union

from fastapi.responses import FileResponse
from fastapi import FastAPI, Body

from app.schemas.api_schemas import UserSchema, UserLoginSchema

app = FastAPI()

users = []


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/forest")
def read_item():
    return FileResponse("resources/forest.png")


@app.post("/user/signup", tags=["user"])
def create_user(user: UserSchema = Body(default=None)):
    users.append(user)
    return {"User created"}


@app.post("/user/login", tags=["user"])
def login_user(user_data: UserLoginSchema = Body(default=None)):
    for user in users:
        if user.email == user_data.email:
            if user.password != user_data.password:
                return {"Error, wrong password!"}
            else:
                # Return signed token
                return {"User logged in!"}
    return {"Error, email not recognized! "}





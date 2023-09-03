import yaml
from fastapi.responses import FileResponse
from fastapi import FastAPI, Body, Depends
import uvicorn

from app.authorization.auth import create_authorization_token, get_password_hash, get_plain_text_password
from app.authorization.bearer import Bearer
from app.schemas.api_schemas import UserSchema, UserLoginSchema

# Load config
with open("conf/config.yaml") as f:
    config = yaml.safe_load(f)

app = FastAPI()

users = []


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/forest", dependencies=[Depends(Bearer())])
def read_item():
    return FileResponse("resources/forest.png")


@app.post("/user/signup", tags=["user"])
def create_user(user: UserSchema = Body(default=None)):
    user.password = get_password_hash(user.password)
    users.append(user)

    return {"User created"}


@app.post("/user/login", tags=["user"])
def login_user(user_data: UserLoginSchema = Body(default=None)):
    for user in users:
        if user.email == user_data.email:
            if not get_plain_text_password(user_data.password, user.password):
                return {"Error, wrong password!"}
            else:
                token = create_authorization_token(user.email, config["TOKEN_VALID_DURATION"],
                                                   config["ALGORITHM"], config["SECRET_KEY"])
                return {"access_token": token, "token_type": "bearer"}
    return {"Error, email not recognized! "}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)



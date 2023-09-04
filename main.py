import yaml

from fastapi.responses import FileResponse
from fastapi import FastAPI, Body, Depends

from app.authorization.auth import create_authorization_token, get_password_hash, get_plain_text_password
from app.authorization.bearer import Bearer
from app.schemas.api_schemas import UserSchema, UserLoginSchema


# Load config
with open("conf/config.yaml") as f:
    config = yaml.safe_load(f)

# App to launch FastAPI
app = FastAPI()

# List of users which acts as a very simply database
users = []


@app.get("/")
def read_root():
    """
    Root endpoint to show hello world

    :return: dictionary with hello world text
    """
    return {"Hello": "World"}


@app.post("/forest", dependencies=[Depends(Bearer())])
def read_item():
    """
    Protected endpoint which can only be accessed if valid token is provided

    :dependencies: Depends on the Bearer class
    :return: An image of a forest iff valid token is provided
    """
    return FileResponse("resources/forest.png")


@app.post("/user/signup", tags=["user"])
def create_user(user: UserSchema = Body(default=None)) -> dict:
    """
    :param user: User in the form of a UserSchema containing sign up information
    :return: Dictionary with either error or success message
    """
    if user.email in [existing_user.email for existing_user in users]:
        return {"Error": "Email already used!"}

    user.password = get_password_hash(user.password)
    users.append(user)

    return {"Success": "User created!"}


@app.post("/user/login", tags=["user"])
def login_user(user_data: UserLoginSchema = Body(default=None)) -> dict:
    """
    Function to authenticate user by logging in

    :param user_data:  User in the form of a UserLoginSchema containing log in information
    :return: Dictionary with either error or success message
    """
    for user in users:
        if user.email == user_data.email:
            if not get_plain_text_password(user_data.password, user.password):
                return {"Error": "wrong password!"}
            else:
                token = create_authorization_token(user.email, config["TOKEN_VALID_DURATION"],
                                                   config["ALGORITHM"], config["SECRET_KEY"])
                return {"access_token": token, "token_type": "bearer"}
    return {"Error": "email not recognized! "}

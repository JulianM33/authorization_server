from datetime import datetime, timedelta
from fastapi import HTTPException

import jwt
import yaml
from jwt import DecodeError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Load config
with open("conf/config.yaml") as f:
    config = yaml.safe_load(f)


def get_plain_text_password(plain_password, hashed_password) -> bool:
    """
    :param plain_password: plaint text password
    :param hashed_password: hashed password
    :return: true iff password is valid, else false
    """
    return pwd_context.verify(plain_password, hash=hashed_password)


def get_password_hash(password) -> str:
    """
    :param password: plain text password
    :return: hashed password
    """
    return pwd_context.hash(password)


def create_authorization_token(email: str, minutes_valid: int, algorithm: str, secret_key: str):
    """
    Creates JWT token based on email and expiration date

    :param email: email acting as a unique identifier
    :param minutes_valid: the amount of minutes the token should be valid
    :param algorithm: algorithm to be used to encode the token
    :param secret_key: secret key to be used to encode the token
    :return: JWT token
    """
    payload = {
        "key": email,
        "expiration_time": (datetime.now() + timedelta(minutes=minutes_valid)).isoformat()
    }
    token = jwt.encode(payload=payload, key=secret_key, algorithm=algorithm)
    return token


def decode_authorization_token(token: str) -> dict:
    """
    :param token: JWT token to be decoded
    :return: the decoded token the decoding is successful and the token is still valid
    """
    try:
        decoded_token = jwt.decode(token, config["SECRET_KEY"], algorithms=config["ALGORITHM"])
        token_date = datetime.fromisoformat(decoded_token["expiration_time"])

        if token_date >= datetime.now():
            return decoded_token
        else:

            raise HTTPException(status_code=403, detail="token is expired!")

    except DecodeError as decode_error:
        raise HTTPException(status_code=404, detail=f"token could not be decoded: {decode_error}")
    except ValueError:
        raise HTTPException(status_code=404, detail=f"date in token is invalid: {decoded_token['expiration_time']}")

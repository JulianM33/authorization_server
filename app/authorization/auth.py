from datetime import datetime, timedelta
import jwt
import yaml
from passlib.context import CryptContext
from typing import Dict

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Load config
with open("conf/config.yaml") as f:
    config = yaml.safe_load(f)


def get_plain_text_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hash=hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_authorization_token(email: str, minutes_valid: int, algorithm: str, secret_key: str):
    payload = {
        "key": email,
        "expiration_time": (datetime.utcnow() + timedelta(minutes=minutes_valid)).isoformat()
    }
    token = jwt.encode(payload=payload, key=secret_key, algorithm=algorithm)
    return token


def decode_authorization_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, config["SECRET_KEY"], algorithms=config["ALGORITHM"])
        token_date = datetime.fromisoformat(decoded_token["expiration_time"])
        return decoded_token if token_date >= datetime.now() else None
    except:
        return {}
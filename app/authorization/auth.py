from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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

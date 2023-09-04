import yaml
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.authorization.auth import decode_authorization_token

security = HTTPBearer()

# Load config
with open("conf/config.yaml") as f:
    config = yaml.safe_load(f)


class Bearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        """
        :param auto_error: set to True such that errors are raised if exceptions occur
        """
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """
        Overridden function from HTTPBearer superclass, with own functionality added
        :param request: FastAPI request object
        :return: valid credentials if token is valid
        """
        credentials: HTTPAuthorizationCredentials = await super(Bearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            self.is_valid_jwt(credentials.credentials)
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def is_valid_jwt(self, jwt_token: str) -> bool:
        """
        :param jwt_token: the JWT token
        :return: True iff JWT token is valid
        """
        payload = decode_authorization_token(jwt_token)
        if payload:
            return True
        else:
            return False

from abc import ABC, abstractmethod
from datetime import timezone, datetime, timedelta

from jose import jwt
from backend.src.config import auth_settings


class AuthRepository(ABC):

    @abstractmethod
    async def create_access_token(self, data: dict) -> str:
        raise NotImplementedError

    # @abstractmethod
    # async def authenticate(self, username: str, password: str) -> str:
    #     raise NotImplementedError
    #
    # @abstractmethod
    # async def verify_token(self, token: str) -> bool:
    #     raise NotImplementedError


class JWTAuthRepository(AuthRepository):

    async def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=30)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, auth_settings.AUTH_SECRET_KEY, algorithm=auth_settings.AUTH_ALGO)
        return encode_jwt

    # async def authenticate(self, username: str, password: str) -> str:
    #     # Perform user authentication (e.g., check username and password against the database)
    #     # If valid, generate JWT token
    #     payload = {"username": username}
    #     token = jwt.encode(payload, self.secret_key, algorithm="HS256")
    #     return token
    #
    # async def verify_token(self, token: str) -> bool:
    #     try:
    #         jwt.decode(token, self.secret_key, algorithms=["HS256"])
    #         return True
    #     except Exception:
    #         return False

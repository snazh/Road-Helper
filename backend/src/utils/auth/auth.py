from abc import ABC, abstractmethod
from datetime import timezone, datetime, timedelta
from typing import Optional, Dict

from fastapi import Request, HTTPException, status, Response
from jose import jwt, JWTError

from backend.src.config import auth_settings


class AuthRepository(ABC):

    @abstractmethod
    async def create_access_token(self, data: dict) -> str:
        raise NotImplementedError

    @abstractmethod
    async def get_token(self, request: Request) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    async def decode_token(self, token: str) -> Optional[Dict]:
        raise NotImplementedError


class JWTAuthRepository(AuthRepository):
    # def __init__(self, credentials):
    #     self.auth_credentials = credentials

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=30)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, auth_settings.AUTH_SECRET_KEY, algorithm=auth_settings.AUTH_ALGO)
        return encode_jwt

    def get_token(self, request: Request) -> Optional[str]:
        token = request.cookies.get("user_access_token")
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token

    def decode_token(self, token: str) -> Optional[Dict]:
        try:
            payload = jwt.decode(token, auth_settings.AUTH_SECRET_KEY, algorithms=[auth_settings.AUTH_ALGO])
            return payload
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

    def delete_token(self, response: Response) -> None:
        response.delete_cookie(key="users_access_token")

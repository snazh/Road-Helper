from backend.src.schemas.user import UserLoginSchema, UserSchemaAdd
from backend.src.services.password import PasswordService
from backend.src.utils.sqlalchemy.repository import SQLAlchemyRepository
from backend.src.utils.auth.auth import JWTAuthRepository
from fastapi import Response, Depends, Request, HTTPException, status


class AuthService:
    def __init__(self, auth_repo, user_repo):
        self.auth_repo: JWTAuthRepository = auth_repo()
        self.users_repo: SQLAlchemyRepository = user_repo()
        self.password_service: PasswordService = PasswordService()

    async def register_user(self, user_data: UserSchemaAdd):
        user_dict = user_data.model_dump()
        user_dict['hashed_password'] = self.password_service.get_password_hash(user_dict['hashed_password'])
        user_id = await self.users_repo.add_one(user_dict)
        return user_id

    async def authenticate_user(self, user_data: UserLoginSchema) -> dict | None:
        user = await self.users_repo.filter(filter_column="username", value=user_data.username)
        is_match = self.password_service.verify_password(plain_password=user_data.password,
                                                         hashed_password=user["hashed_password"])
        if user is None or not is_match:
            return None
        else:
            return user

    async def authorize_user(self, user_data: UserLoginSchema, response: Response) -> dict | None:
        user = await self.authenticate_user(user_data)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
        access_token = self.auth_repo.create_access_token({"sub": user["username"]})
        response.set_cookie(key="user_access_token", value=access_token, httponly=True)
        return {
            'access_token': access_token,
            'refresh_token': None
        }

    async def logout(self, response: Response) -> None:
        self.auth_repo.delete_token(response)

    async def get_current_user(self, request: Request) -> dict:

        token = self.auth_repo.get_token(request)
        payload = self.auth_repo.decode_token(token)

        user = await self.users_repo.filter(filter_column="username", value=payload['sub'])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

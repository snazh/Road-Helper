from backend.src.models.user_model import User
from backend.src.schemas.user import UserLoginSchema, UserSchemaAdd
from backend.src.services.password import PasswordService
from backend.src.utils.sqlalchemy.repository import SQLAlchemyRepository
from backend.src.utils.auth.auth import JWTAuthRepository
from fastapi import Response


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
        print(user)
        is_match = self.password_service.verify_password(plain_password=user_data.password,
                                                         hashed_password=user["hashed_password"])
        if user is None or not is_match:
            return None

        else:
            return user

    async def authorize_user(self, user_data: UserLoginSchema, response: Response):
        user = await self.authenticate_user(user_data)
        if user is None:
            print(False)
            return None
        access_token = await self.auth_repo.create_access_token({"sub": user["id"]})
        response.set_cookie(key="users_access_token", value=access_token, httponly=True)
        return {
            'access_token': access_token,
            'refresh_token': None
        }

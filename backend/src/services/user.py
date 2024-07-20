from typing import List

from backend.src.schemas.user import UserSchemaAdd, UserLoginSchema
from backend.src.services.password import PasswordService
from backend.src.utils.sqlalchemy.repository import SQLAlchemyRepository


class UsersService:
    def __init__(self, users_repo):
        self.users_repo: SQLAlchemyRepository = users_repo()
        self.password_service: PasswordService = PasswordService()

    async def add_user(self, user: UserSchemaAdd) -> int:
        user_dict = user.model_dump()
        user_dict['password'] = self.password_service.get_password_hash(user_dict['password'])
        user_id = await self.users_repo.add_one(user_dict)
        return user_id



    async def get_all_users(self) -> List[dict]:
        users = await self.users_repo.get_all()
        return users

    async def get_specific_user(self, user_id: int) -> dict:
        user = await self.users_repo.get_one(user_id)
        return user

    # async def get_user_by_name(self, username: str) -> dict:
    #     user = await self.users_repo.filter(filter_column="username", value=username)
    #     return user

    async def delete_user(self, user_id: int) -> None:
        user = await self.users_repo.get_one(user_id)

        await self.users_repo.delete_one(user_id)
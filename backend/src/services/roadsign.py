from backend.src.schemas.roadsign import RoadSignSchemaAdd
from backend.src.utils.sqlalchemy.repository import SQLAlchemyRepository


class RoadSignsService:
    def __init__(self, roadsigns_repo):
        self.signs_repo: SQLAlchemyRepository = roadsigns_repo()

    async def add_sign(self, sign: RoadSignSchemaAdd):
        signs_dict = sign.model_dump()
        sign_id = await self.signs_repo.add_one(signs_dict)
        return sign_id

    async def get_all_signs(self):
        signs = await self.signs_repo.get_all()
        return signs

    async def get_specific_sign(self, sign_id: int):
        sign = await self.signs_repo.get_one(sign_id)
        return sign

    async def delete_sign(self, sign_id: int) -> None:
        sign = await self.signs_repo.get_one(sign_id)

        await self.signs_repo.delete_one(sign_id)

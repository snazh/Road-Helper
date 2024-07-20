from abc import ABC, abstractmethod

from sqlalchemy import insert, select, delete

from backend.src.database.connection import async_session_maker


class AbstractRepository(ABC):  # Abstract layer for CRUD initialization
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, entity_id: int):
        return NotImplementedError

    @abstractmethod
    async def delete_one(self, entity_id: int):
        return NotImplementedError

    @abstractmethod
    async def filter(self, filter_column: str, value: str):
        return NotImplementedError


# repository for basic CRUD operations
class SQLAlchemyRepository(AbstractRepository):
    model = None

    def _to_dict(self, entity):
        """Convert SQLAlchemy model instance to dictionary"""
        return {column.name: getattr(entity, column.name) for column in entity.__table__.columns}

    async def add_one(self, data: dict) -> int:  # returns record's pk
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    async def get_all(self) -> list[dict]:  # returns all records
        async with async_session_maker() as session:
            stmt = select(self.model)
            result = await session.execute(stmt)
            result = [row[0] for row in result.all()]
            return result

    async def get_one(self, entity_id: int) -> dict | None:  # returns specific record
        async with async_session_maker() as session:
            query = select(self.model).where(self.model.id == entity_id)
            result = await session.execute(query)
            entity = result.scalar_one_or_none()
            return entity

    async def delete_one(self, entity_id: int) -> None:  # delete specific record
        async with async_session_maker() as session:
            stmt = delete(self.model).where(self.model.id == entity_id)
            await session.execute(stmt)
            await session.commit()

    async def filter(self, filter_column: str, value: str) -> dict | None:
        async with async_session_maker() as session:
            query = select(self.model).where(getattr(self.model, filter_column) == value)
            result = await session.execute(query)
            entity = result.scalar_one_or_none()
            if entity:
                return self._to_dict(entity)
            return None

    async def update_one(self, entity_id):  # todo
        pass

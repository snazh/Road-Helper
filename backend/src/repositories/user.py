from backend.src.models.user_model import User
from backend.src.utils.sqlalchemy.repository import SQLAlchemyRepository


# User repository creation
class UserRepository(SQLAlchemyRepository):
    model = User

from backend.src.models.roadsigns_model import RoadSign
from backend.src.utils.sqlalchemy.repository import SQLAlchemyRepository


# Road sign repository creation
class RoadSignsRepository(SQLAlchemyRepository):
    model = RoadSign

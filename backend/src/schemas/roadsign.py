

from pydantic import BaseModel


class RoadSignSchema(BaseModel):
    id: int
    name: str
    description: str
    image_url: str

    class Config:
        from_attributes = True


class RoadSignSchemaAdd(BaseModel):
    name: str
    description: str
    image_url: str

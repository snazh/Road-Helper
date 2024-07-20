from pydantic import BaseModel, EmailStr, Field, field_validator


class UserSchemaBase(BaseModel):
    username: str = Field(min_length=5, max_length=30, description="Username")

    class Config:
        from_attributes = True


class UserSchemaShow(UserSchemaBase):
    id: int
    email: str
    avatar: str


class UserSchemaAdd(UserSchemaBase):

    email: EmailStr = Field(..., description="Electronic mail")
    avatar: str
    hashed_password: str

    class Config:
        from_attributes = True
    # @field_validator("phone_number")
    # @classmethod
    # def validate_phone_number(cls, value: str) -> str:
    #     if not re.match(r'^\+\d{5,15}$', value):
    #         raise ValueError('Номер телефона должен начинаться с "+" и содержать от 5 до 15 цифр')
    #     return value


class UserLoginSchema(UserSchemaBase):
    password: str



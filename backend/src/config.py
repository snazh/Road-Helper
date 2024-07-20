from pydantic_settings import BaseSettings, SettingsConfigDict
import os

# declaring path to .env file
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(base_dir, '.env')


class CoreSettings(BaseSettings):
    model_config = SettingsConfigDict(  # configuring .env file
        env_file=env_path,
        env_file_encoding='utf-8',
        extra="ignore")  # ignoring other secret keys )


# Postgres SQL credentials unpacking
class DBSettings(CoreSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def async_database_url(self) -> str:
        # Construct the async database URL
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?async_fallback=True"


# AWS S3 Bucket credentials unpacking
class S3BucketSettings(CoreSettings):
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_S3_BUCKET_NAME: str
    AWS_REGION: str
    AWS_ENDPOINT_URL: str


class AuthSettings(CoreSettings):
    AUTH_SECRET_KEY: str
    REFRESH_AUTH_SECRET_KEY: str
    AUTH_ALGO: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int


db_settings = DBSettings()
s3bucket_settings = S3BucketSettings()
auth_settings = AuthSettings()

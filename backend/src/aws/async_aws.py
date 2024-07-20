from contextlib import asynccontextmanager
from aiobotocore.session import get_session
from backend.src.config import s3bucket_settings as bucket


class S3Client:
    def __init__(self, access_key: str, secret_key: str, endpoint_url: str, bucket_name: str, region: str):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "region_name": region,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self, file_path: str, object_name: str = None):
        if object_name is None:
            object_name = file_path.split("/")[-1]
        async with self.get_client() as client:
            with open(file_path, "rb") as file:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file
                )


async def main():
    s3_client = S3Client(
        access_key=bucket.AWS_ACCESS_KEY,
        secret_key=bucket.AWS_SECRET_KEY,
        endpoint_url=bucket.AWS_ENDPOINT_URL,
        bucket_name=bucket.AWS_S3_BUCKET_NAME,
        region=bucket.AWS_REGION
    )
    await s3_client.upload_file("pizza.jpg")

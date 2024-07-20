import boto3
from backend.src.config import s3bucket_settings as bucket


class SyncS3Client:
    def __init__(self, access_key, region, secret_key, bucket_name):
        self.config = {
            "access_key": access_key,
            "secret_key": secret_key,
            "region": region
        }
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            service_name="s3",
            region_name=self.config["region"],
            aws_access_key_id=self.config["access_key"],
            aws_secret_access_key=self.config["secret_key"]
        )

    def upload(self, file_path):
        self.s3_client.upload_file(file_path, bucket.AWS_S3_BUCKET_NAME, file_path)

    def download(self, file_path, download_path):
        self.s3_client.download_file(self.bucket_name, file_path, download_path)

    def unload(self, file_path):
        s3_client = boto3.client(
            service_name="s3",
            region_name=self.config["region"],
            aws_access_key_id=self.config["access_key"],
            aws_secret_access_key=self.config["secret_key"]
        )
        try:
            response = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': file_path},
                ExpiresIn=3600  # URL expiration time in seconds (1 hour in this case)
            )
            return response
        except Exception as e:
            print(f"Error generating URL for file '{file_path}': {str(e)}")
            return None


aws_s3_client = SyncS3Client(
    access_key=bucket.AWS_ACCESS_KEY,
    secret_key=bucket.AWS_SECRET_KEY,
    region=bucket.AWS_REGION,
    bucket_name=bucket.AWS_S3_BUCKET_NAME
)
# aws_s3_client.download("pizza.jpg", "downloaded_pizza.jpg")
# aws_s3_client.upload("pizza.jpg")
print(aws_s3_client.unload("pizza.jpg"))

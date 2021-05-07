import datetime
import mimetypes
import os
import uuid

import boto3

from config import S3Config

CONFIG = S3Config()


async def get_upload_location(filename):
    extension = os.path.splitext(filename)[-1]
    timeslash = datetime.datetime.now().strftime('%Y/%m/%d')
    return f'media/{timeslash}/{uuid.uuid4().hex}{extension}'


async def upload_to_bucket(file_obj, name):
    s3 = boto3.resource(
        's3',
        aws_access_key_id=CONFIG.AWS_ACCESS_KEY,
        aws_secret_access_key=CONFIG.AWS_SECRET_KEY,
    )
    content_type, __ = mimetypes.guess_type(name, strict=False)
    s3_uploaded_obj = s3.Bucket(CONFIG.AWS_S3_BUCKET_NAME_STATIC).put_object(
        Key=await get_upload_location(name),
        Body=file_obj,
        ContentType=content_type
    )
    return CONFIG.AWS_S3_PUBLIC_URL, s3_uploaded_obj.key

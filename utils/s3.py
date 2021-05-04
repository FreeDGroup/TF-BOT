import datetime
import mimetypes
import os
import uuid

import boto3

from config import S3Config

CONFIG = S3Config()


def upload_location(instance, filename):
    extension = os.path.splitext(filename)[-1]
    timeslash = datetime.datetime.now().strftime('%Y/%m/%d')
    return f'media/{timeslash}/{uuid.uuid4().hex}{extension}'


def upload_to_bucket(file_obj):
    s3 = boto3.resource('s3')
    content_type, __ = mimetypes.guess_type(file_obj.name, strict=False)
    s3_uploaded_obj = s3.Bucket(CONFIG.AWS_S3_BUCKET_NAME_STATIC).put_object(
        Key=upload_location(file_obj, file_obj.name),
        Body=file_obj,
        ContentType=content_type
    )
    return CONFIG.AWS_S3_PUBLIC_URL, s3_uploaded_obj.key

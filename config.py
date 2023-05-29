#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os


class DefaultConfig:
    """Bot Configuration"""

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    TENANT_ID = os.environ.get("TENANT_ID", "")
    CONNECTION_NAME = os.environ.get("CONNECTION_NAME", "francis-bot")
    OPENAI_SECRET_KEY = os.environ.get("OPENAI_SECRET_KEY", "")


class S3Config:
    AWS_S3_BUCKET_NAME_STATIC = "flanb-delivery-static"
    AWS_S3_PUBLIC_URL = "https://delivery-static.arabiz.live/"
    AWS_ACCESS_KEY = os.environ.get("aws_access_key_id", "")
    AWS_SECRET_KEY = os.environ.get("aws_secret_access_key", "")

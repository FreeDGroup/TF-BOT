# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import io
import os
import urllib.parse
import urllib.request
import base64
import json

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext, CardFactory
from botbuilder.schema import (
    ChannelAccount,
    HeroCard,
    CardAction,
    ActivityTypes,
    Attachment,
    AttachmentData,
    Activity,
    ActionTypes,
)

from utils.s3 import upload_to_bucket


class AttachmentsHandler:
    """
    Represents a bot that processes incoming activities.
    For each user interaction, an instance of this class is created and the OnTurnAsync method is called.
    This is a Transient lifetime service. Transient lifetime services are created
    each time they're requested. For each Activity received, a new instance of this
    class is created. Objects that are expensive to construct, or have a lifetime
    beyond the single turn, should be carefully managed.
    """

    async def _handle_incoming_attachment(self, turn_context: TurnContext):
        for attachment in turn_context.activity.attachments:
            data = await self._get_file_object_by_attachment(attachment)
            if data:
                url, path = await upload_to_bucket(data, attachment.name)
                await turn_context.send_activity(
                    f"업로드 링크 : {url}{path}"
                )
            else:
                await turn_context.send_activity(
                    f"업로드가 불가능한 파일 형식입니다"
                )

    async def _get_file_object_by_attachment(self, attachment: Attachment):
        try:
            # url = 'https://' + \
            #     urllib.parse.quote(attachment.content_url.split('https://')[1])
            # headers = {'User-Agent': 'Mozilla/5.0'}
            # req = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(
                attachment.content['downloadUrl'])
            headers = response.info()

            # If user uploads JSON file, this prevents it from being written as
            # "{"type":"Buffer","data":[123,13,10,32,32,34,108..."
            if headers["content-type"] == "application/json":
                data = bytes(json.load(response)["data"])
            else:
                data = response.read()

            return io.BytesIO(data)
        except Exception as exception:
            print(exception)
            return None

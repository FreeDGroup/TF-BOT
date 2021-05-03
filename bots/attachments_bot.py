# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

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
        """
        Handle attachments uploaded by users. The bot receives an Attachment in an Activity.
        The activity has a List of attachments.
        Not all channels allow users to upload files. Some channels have restrictions
        on file type, size, and other attributes. Consult the documentation for the channel for
        more information. For example Skype's limits are here
        <see ref="https://support.skype.com/en/faq/FA34644/skype-file-sharing-file-types-size-and-time-limits"/>.
        :param turn_context:
        :return:
        """
        for attachment in turn_context.activity.attachments:
            attachment_info = await self._download_attachment_and_write(attachment)
            if "filename" in attachment_info:
                await turn_context.send_activity(
                    f"Attachment {attachment_info['filename']} has been received to {attachment_info['local_path']}"
                )

    async def _download_attachment_and_write(self, attachment: Attachment) -> dict:
        """
        Retrieve the attachment via the attachment's contentUrl.
        :param attachment:
        :return: Dict: keys "filename", "local_path"
        """
        try:
            response = urllib.request.urlopen(attachment.content_url)
            headers = response.info()

            # If user uploads JSON file, this prevents it from being written as
            # "{"type":"Buffer","data":[123,13,10,32,32,34,108..."
            if headers["content-type"] == "application/json":
                data = bytes(json.load(response)["data"])
            else:
                data = response.read()

            local_filename = os.path.join(os.getcwd(), attachment.name)
            with open(local_filename, "wb") as out_file:
                out_file.write(data)

            return {"filename": attachment.name, "local_path": local_filename}
        except Exception as exception:
            print(exception)
            return {}

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from bots.handlers.attachments import AttachmentsHandler
from bots.handlers.helpers import HelpersHandler
from bots.handlers.welcomes import WelcomesHandler
from botbuilder.core import ActivityHandler, TurnContext


class MyBot(
    AttachmentsHandler,
    HelpersHandler,
    WelcomesHandler,
    ActivityHandler
):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        if (
            turn_context.activity.attachments
            and len(turn_context.activity.attachments) > 0
        ):
            await self._handle_incoming_attachment(turn_context)
        else:
            if turn_context.activity.text == '/':
                await self._send_help_message(turn_context)
            elif turn_context.activity.text == '/날씨':
                await turn_context.send_activity(f"TODO")
            elif turn_context.activity.text == '/미세먼지':
                await turn_context.send_activity(f"TODO")
            else:
                await turn_context.send_activity(f"/")

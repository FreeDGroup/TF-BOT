# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from bots.handlers.attachments import AttachmentsHandler
from bots.handlers.welcomes import WelcomesHandler
from botbuilder.core import ActivityHandler, TurnContext


class MyBot(
    AttachmentsHandler,
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
                await turn_context.send_activity(
                    """
                    도움말:
                    /날씨
                    /미세먼지
                    이미지 첨부: 이미지를 전송하면 공유가능한 링크가 반환됩니다.
                    """
                )
            elif turn_context.activity.text == '/날씨':
                await turn_context.send_activity(f"TODO")
            elif turn_context.activity.text == '/미세먼지':
                await turn_context.send_activity(f"TODO")
            else:
                await turn_context.send_activity(f"/")

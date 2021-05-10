# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from bots.handlers.attachments import AttachmentsHandler
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount


class MyBot(AttachmentsHandler, ActivityHandler):
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
                    "도움말:\n"
                    + "/날씨\n"
                    + "/미세먼지\n"
                    + "이미지 첨부: 이미지를 전송하면 공유가능한 링크가 반환됩니다."
                )
            elif turn_context.activity.text == '/날씨':
                await turn_context.send_activity(f"TODO")
            elif turn_context.activity.text == '/미세먼지':
                await turn_context.send_activity(f"TODO")
            else:
                await turn_context.send_activity(f"/")

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        await self._send_welcome_message(turn_context)

    async def _send_welcome_message(self, turn_context: TurnContext):
        """
        Greet the user and give them instructions on how to interact with the bot.: param turn_context:: return:
        """
        for member in turn_context.activity.members_added:
            if member.id != turn_context.activity.recipient.id:
                print(member)
                await turn_context.send_activity(
                    f"안녕하세요 {member.name} 님"
                )

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from utils.attachments import AttachmentHandler
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount


class MyBot(AttachmentHandler, ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        if (
            turn_context.activity.attachments
            and len(turn_context.activity.attachments) > 0
        ):
            await self._handle_incoming_attachment(turn_context)
        else:
            await self._handle_outgoing_attachment(turn_context)

        if turn_context.activity.text == "파일":
            await self._display_options(turn_context)
        await turn_context.send_activity(f"따라하기 '{ turn_context.activity.text }'")

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        await self._send_welcome_message(turn_context)

    async def _send_welcome_message(self, turn_context: TurnContext):
        """
        Greet the user and give them instructions on how to interact with the bot.
        :param turn_context:
        :return:
        """
        for member in turn_context.activity.members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    f"{member.name} 님. 저는 Francis 봇입니다."
                )

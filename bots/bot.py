# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext

from bots.handlers.attachments import AttachmentsHandler
from bots.handlers.helpers import HelpersHandler
from bots.handlers.meetings import MeetingsHandler
from bots.handlers.welcomes import WelcomesHandler


class MyBot(WelcomesHandler, ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        if (
            turn_context.activity.attachments
            and len(turn_context.activity.attachments) > 0
            and turn_context.activity.attachments[0].content_type != "text/html"
        ):
            await AttachmentsHandler().handle_incoming_attachment(turn_context)
        else:
            if "<at>Francis 봇</at>" in turn_context.activity.text:
                text = turn_context.activity.text.split("<at>Francis 봇</at>")[1].strip()
            else:
                text = turn_context.activity.text
            if text == "/":
                await HelpersHandler().send_help_message(turn_context)
            elif text.startswith("/회의실"):
                await MeetingsHandler().handle(turn_context)
            elif text == "/날씨":
                await turn_context.send_activity("TODO")
            elif text == "/미세먼지":
                await turn_context.send_activity("TODO")
            else:
                await turn_context.send_activity("아직 등록되지 않은 명령어입니다. 도움이 필요하시면 `/` 를 입력해주세요")

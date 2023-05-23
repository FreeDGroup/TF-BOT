from typing import List

from botbuilder.core import (
    ConversationState,
    TurnContext,
    UserState,
)
from botbuilder.core.teams import TeamsActivityHandler
from botbuilder.dialogs import Dialog
from botbuilder.schema import ChannelAccount

from bots.handlers.attachments import AttachmentsHandler
from bots.handlers.helpers import HelpersHandler
from bots.handlers.meetings import MeetingsHandler
from bots.handlers.welcomes import WelcomesHandler
from utils.dialog_helper import DialogHelper


class MyBot(WelcomesHandler, TeamsActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        dialog: Dialog,
    ):
        self.conversation_state = conversation_state
        self.user_state = user_state
        self.dialog = dialog

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # Save any state changes that might have occurred during the turn.
        await self.conversation_state.save_changes(turn_context, False)
        await self.user_state.save_changes(turn_context, False)

    # async def on_message_activity(self, turn_context: TurnContext):
    #     await DialogHelper.run_dialog(
    #         self.dialog,
    #         turn_context,
    #         self.conversation_state.create_property("DialogState"),
    #     )

    async def on_members_added_activity(self, members_added: List[ChannelAccount], turn_context: TurnContext):
        for member in members_added:
            # Greet anyone that was not the target (recipient) of this message.
            # To learn more about Adaptive Cards, see https://aka.ms/msbot-adaptivecards for more details.
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "Welcome to Authentication Bot on MSGraph. Type anything to get logged in. Type 'logout' to "
                    "sign-out. "
                )

    async def on_token_response_event(self, turn_context: TurnContext):
        # Run the Dialog with the new Token Response Event Activity.
        await DialogHelper.run_dialog(
            self.dialog,
            turn_context,
            self.conversation_state.create_property("DialogState"),
        )

    async def on_teams_signin_verify_state(self, turn_context: TurnContext):
        # Running dialog with Teams Signin Verify State Activity.
        await DialogHelper.run_dialog(
            self.dialog,
            turn_context,
            self.conversation_state.create_property("DialogState"),
        )

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

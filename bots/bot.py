import traceback
from typing import List

from botbuilder.core import (
    ConversationState,
    TurnContext,
    UserState,
)
from botbuilder.core.teams import TeamsActivityHandler
from botbuilder.dialogs import DialogSet
from botbuilder.schema import ChannelAccount

from dialogs.attachments import AttachmentsHandler
from dialogs.calendar_dialog import CalendarDialog
from dialogs.main_dialog import MainDialog
from utils import openai_helper
from utils.dialog_helper import DialogHelper


class MyBot(TeamsActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        dialogs: DialogSet,
    ):
        self.conversation_state = conversation_state
        self.user_state = user_state
        self.dialogs = dialogs

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # Save any state changes that might have occurred during the turn.
        await self.conversation_state.save_changes(turn_context, False)
        await self.user_state.save_changes(turn_context, False)

    async def on_members_added_activity(self, members_added: List[ChannelAccount], turn_context: TurnContext):
        for member in members_added:
            # Greet anyone that was not the target (recipient) of this message.
            # To learn more about Adaptive Cards, see https://aka.ms/msbot-adaptivecards for more details.
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("안녕하세요 저는 francis 봇입니다. 초기 로그인을 위해 아무 글자나 입력해주세요")

    async def on_token_response_event(self, turn_context: TurnContext):
        # Run the Dialog with the new Token Response Event Activity.
        self.conversation_state.create_property("DialogState")
        await DialogHelper.run_dialog(
            MainDialog.__name__,
            self.dialogs,
            turn_context,
        )

    async def on_teams_signin_verify_state(self, turn_context: TurnContext):
        # Running dialog with Teams Signin Verify State Activity.
        self.conversation_state.create_property("DialogState")
        await DialogHelper.run_dialog(
            MainDialog.__name__,
            self.dialogs,
            turn_context,
        )

    async def on_message_activity(self, turn_context: TurnContext):
        try:
            if (
                turn_context.activity.attachments
                and len(turn_context.activity.attachments) > 0
                and turn_context.activity.attachments[0].content_type != "text/html"
            ):
                await AttachmentsHandler().handle_incoming_attachment(turn_context)
            else:
                if "<at>Francis 봇</at>" in turn_context.activity.text:
                    turn_context.activity.text = turn_context.activity.text.split("<at>Francis 봇</at>")[1].strip()
                else:
                    turn_context.activity.text = turn_context.activity.text
                ai_parsed_category = openai_helper.get_parsed_question_category(turn_context.activity.text)
                if type(ai_parsed_category) == int and int(ai_parsed_category) == 1:
                    self.conversation_state.create_property("DialogState")
                    await DialogHelper.run_dialog(
                        CalendarDialog.__name__,
                        self.dialogs,
                        turn_context,
                    )
                else:
                    await turn_context.send_activity("아직 도와드릴 수 없는 질문입니다. 다른 질문을 해주세요. category: {ai_parsed_category}")
        except Exception as e:
            error_traceback = traceback.format_exc()

            await turn_context.send_activity(f"오류가 발생했습니다. {str(e)}\n{error_traceback}")
            # else:
            #     # 사용자가 로그인된 경우의 로직
            #     await turn_context.send_activity(f"안녕하세요, {user_profile.name} 님!")

            # if text == "/":
            #     await HelpersHandler().send_help_message(turn_context)
            # elif text.startswith("/회의실"):
            #     await MeetingsHandler(self.dialog, self.conversation_state).handle(turn_context)
            # elif text == "/날씨":
            #     await turn_context.send_activity("TODO")
            # elif text == "/미세먼지":
            #     await turn_context.send_activity("TODO")
            # else:
            #     await turn_context.send_activity("아직 등록되지 않은 명령어입니다. 도움이 필요하시면 `/` 를 입력해주세요")

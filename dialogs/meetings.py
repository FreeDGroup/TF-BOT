from botbuilder.core import TurnContext

from dialogs import oauth
from utils.dialog_helper import DialogHelper


class MeetingsHandler:
    def __init__(self, dialog, conversation_state):
        self.dialog = dialog
        self.conversation_state = conversation_state

    async def handle(self, turn_context: TurnContext):
        await turn_context.send_activity("회의실 예약을 시작합니다")
        await oauth.send_oauth_card(turn_context)
        await DialogHelper.run_dialog(
            self.dialog,
            turn_context,
            self.conversation_state.create_property("DialogState"),
        )

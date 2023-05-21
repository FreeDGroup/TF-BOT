from botbuilder.core import TurnContext

from bots.handlers import oauth


class MeetingsHandler:
    async def handle(self, turn_context: TurnContext):
        await turn_context.send_activity("회의실 예약을 시작합니다")
        await oauth.send_oauth_card(turn_context)

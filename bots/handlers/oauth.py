from botbuilder.core import CardFactory, MessageFactory
from botbuilder.schema import ActionTypes, CardAction, OAuthCard

from config import DefaultConfig

CONFIG = DefaultConfig()


async def send_oauth_card(turn_context):
    # Microsoft Azure에서 등록한 앱의 OAuth 설정에 따라 이 부분을 수정해야 합니다.
    connection_name = "francis bot oauth"

    # OAuthCard 생성
    card = OAuthCard(
        text="로그인이 필요합니다.",
        connection_name=connection_name,
        buttons=[CardAction(type=ActionTypes.signin, title="로그인", value="signin")],
    )

    # 메시지에 OAuthCard를 추가하고 사용자에게 보냅니다.
    await turn_context.send_activity(MessageFactory.attachment(CardFactory.signin_card(card)))

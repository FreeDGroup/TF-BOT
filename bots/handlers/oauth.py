from botbuilder.core import CardFactory, MessageFactory
from botbuilder.schema import ActionTypes, CardAction, SigninCard

from config import DefaultConfig


async def send_oauth_card(turn_context):
    # Microsoft Azure에서 등록한 앱의 OAuth 설정에 따라 이 부분을 수정해야 합니다.

    # OAuthCard 생성
    card = SigninCard(
        text="로그인이 필요합니다.",
        buttons=[
            CardAction(
                title="로그인",
                type=ActionTypes.signin,
                value=f"https://login.microsoftonline.com/{DefaultConfig.TENANT_ID}/oauth2/v2.0/authorize?response_type=code&client_id=a795c2b9-3815-4cda-b80a-0d0cb8ad6109&redirect_uri=localhost:8000&state=12345&prompt=consent"
                # 이 value 값은 실제 OAuth 설정에 맞게 변경해야 합니다.
            )
        ],
    )

    # 메시지에 OAuthCard를 추가하고 사용자에게 보냅니다.
    await turn_context.send_activity(MessageFactory.attachment(CardFactory.signin_card(card)))

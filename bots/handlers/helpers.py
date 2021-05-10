from botbuilder.core import CardFactory, MessageFactory, TurnContext
from botbuilder.schema import (
    HeroCard,
    CardImage,
    CardAction,
    ActionTypes,
)


class HelpersHandler:

    async def _send_help_message(self, turn_context: TurnContext):
        card = HeroCard(
            title=f"도움말",
            text="이미지를 전송하면 공유가능한 링크가 반환됩니다.",
            images=[CardImage(url="https://aka.ms/bf-welcome-card-image")],
            buttons=[
                CardAction(
                    type=ActionTypes.post_back,
                    title="/날씨",
                    text="/날씨",
                    display_text="/날씨",
                    value="/날씨",
                ),
                CardAction(
                    type=ActionTypes.post_back,
                    title="/미세먼지",
                    text="/미세먼지",
                    display_text="/미세먼지",
                    value="/미세먼지",
                ),
            ],
        )

        return await turn_context.send_activity(
            MessageFactory.attachment(CardFactory.hero_card(card))
        )

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import (
    DialogTurnResult,
    WaterfallDialog,
    WaterfallStepContext,
)
from botbuilder.dialogs.prompts import ConfirmPrompt, OAuthPrompt, OAuthPromptSettings

from dialogs.logout_dialog import LogoutDialog


class MainDialog(LogoutDialog):
    def __init__(self, connection_name: str):
        super().__init__(MainDialog.__name__, connection_name)

        self.add_dialog(
            OAuthPrompt(
                OAuthPrompt.__name__,
                OAuthPromptSettings(
                    connection_name=connection_name,
                    text="로그인이 필요합니다",
                    title="로그인",
                    timeout=300000,
                ),
            )
        )

        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))

        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.prompt_step,
                    self.login_step,
                ],
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def prompt_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.begin_dialog(OAuthPrompt.__name__)

    async def login_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not step_context.result:
            await step_context.context.send_activity("로그인에 실패했습니다 다시 시도해주세요.")
        return await step_context.end_dialog()

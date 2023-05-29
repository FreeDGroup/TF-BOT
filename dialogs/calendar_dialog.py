# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import UserState
from botbuilder.dialogs import (
    DialogTurnResult,
    WaterfallDialog,
    WaterfallStepContext,
)

from dialogs.main_dialog import MainDialog
from utils import graph


class CalendarDialog(MainDialog):
    def __init__(self, connection_name: str, user_state: UserState):
        super().__init__(CalendarDialog.__name__, connection_name, user_state)

        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.prompt_step,
                    self.login_step,
                    self.test_step,
                ],
            )
        )

    async def test_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if step_context.result:
            token = step_context.result
            result = graph.get_meetings(token, "meeting.room.2f@freedgrouptech.com")
            await step_context.context.send_activity(result)
        return await step_context.end_dialog()

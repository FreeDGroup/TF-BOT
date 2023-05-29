# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import UserState
from botbuilder.dialogs import (
    DialogTurnResult,
    WaterfallDialog,
    WaterfallStepContext,
)

from dialogs.main_dialog import MainDialog
from utils import graph, openai


class CalendarDialog(MainDialog):
    def __init__(self, connection_name: str, user_state: UserState):
        super().__init__(CalendarDialog.__name__, connection_name, user_state)

        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.prompt_step,
                    self.login_step,
                    self.calendar_step,
                ],
            )
        )

    async def calendar_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if step_context.result:
            token = step_context.result
            if step_context.values["user_input"].startswith("2층"):
                result = graph.get_meetings(token, "meeting.room.2f@freedgrouptech.com")
            elif step_context.values["user_input"].startswith("3층"):
                result = graph.get_meetings(token, "meeting.room.3f@freedgrouptech.com")
            elif step_context.values["user_input"].startswith("4층"):
                result = graph.get_meetings(token, "meeting.room.4f@freedgrouptech.com")
            elif step_context.values["user_input"].startswith("5층"):
                result = graph.get_meetings(token, "meeting.room.5f@freedgrouptech.com")
            else:
                return await step_context.end_dialog()

            ai_generated = openai.get_meeting_schedule(result, step_context.values["user_input"])
            await step_context.context.send_activity(ai_generated)

        return await step_context.end_dialog()

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import UserState
from botbuilder.dialogs import (
    DialogTurnResult,
    WaterfallDialog,
    WaterfallStepContext,
)

from dialogs.main_dialog import MainDialog
from utils import graph, openai_helper


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

            await step_context.context.send_activity("답변을 준비중입니다.")
            ai_generated = openai_helper.get_meeting_schedule(result, "오늘 미팅룸 사용가능한 시간 알려줘")
            await step_context.context.send_activity(ai_generated)

        return await step_context.end_dialog()

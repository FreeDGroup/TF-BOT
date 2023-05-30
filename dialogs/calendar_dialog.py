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


import datetime

# Graph API로부터 받아온 데이터 예시
meetings = [{"start": "2023-05-29T15:30:00.0000000", "end": "2023-05-29T16:00:00.0000000"}, 
            {"start": "2023-05-29T17:00:00.0000000", "end": "2023-05-29T18:30:00.0000000"},]

# 시간 데이터 파싱 예시
parsed_meetings = [(datetime.datetime.fromisoformat(meeting['start'].replace('0.0000000', '')), 
                    datetime.datetime.fromisoformat(meeting['end'].replace('0.0000000', ''))) for meeting in meetings]

# 팀즈앱에 대한 질문 처리 함수
def process_question(floor):
    n_meetings = len(parsed_meetings)
    if n_meetings > 0:
        time_ranges = ', '.join([f"{start.strftime('%H시%M분')}~{end.strftime('%H시%M분')}" for start, end in parsed_meetings])
        answer = f"{floor}층 미팅룸은 오늘 {n_meetings}개의 예약이 있으며 사용 시간은 {time_ranges} 입니다."
    else:
        answer = f"{floor}층 미팅룸은 오늘 예약이 없습니다."
    return answer


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

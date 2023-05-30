# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# Graph API로부터 받아온 데이터 예시
# meetings = [{"start": "2023-05-29T15:30:00.0000000", "end": "2023-05-29T16:00:00.0000000"},
#             {"start": "2023-05-29T17:00:00.0000000", "end": "2023-05-29T18:30:00.0000000"},]
# # 시간 데이터 파싱 예시
# parsed_meetings = [(datetime.datetime.fromisoformat(meeting['start'].replace('0.0000000', '')),
#                     datetime.datetime.fromisoformat(meeting['end'].replace('0.0000000', ''))) for meeting in meetings]
# 팀즈앱에 대한 질문 처리 함수
import datetime

from botbuilder.core import UserState
from botbuilder.dialogs import (
    DialogTurnResult,
    WaterfallDialog,
    WaterfallStepContext,
)

from dialogs.main_dialog import MainDialog
from utils import graph, openai_helper


def process_question(floor: int, q_datetime: str, meetings: list):
    # Query datetime
    query_datetime = datetime.datetime.fromisoformat(q_datetime).astimezone(
        datetime.timezone(datetime.timedelta(hours=9))
    )

    # Parsing meetings
    parsed_meetings = [
        (
            datetime.datetime.fromisoformat(meeting["start"].replace(".0000000", "")).astimezone(
                datetime.timezone(datetime.timedelta(hours=9))
            ),
            datetime.datetime.fromisoformat(meeting["end"].replace(".0000000", "")).astimezone(
                datetime.timezone(datetime.timedelta(hours=9))
            ),
        )
        for meeting in meetings
    ]

    # Filtering meetings
    filtered_meetings = [(start, end) for start, end in parsed_meetings if start >= query_datetime]
    n_meetings = len(filtered_meetings)

    if n_meetings > 0:
        time_ranges = ", ".join(
            [f"{start.strftime('%H시%M분')}~{end.strftime('%H시%M분')}" for start, end in filtered_meetings]
        )
        answer = f"{floor}층 미팅룸에는 {query_datetime.strftime('%d일 %H시%M분')} 이후 {n_meetings}개의 예약이 있으며 사용 시간은 {time_ranges} 입니다."  # noqa: E501
    else:
        answer = f"{floor}층 미팅룸에는 {query_datetime.strftime('%Y년 %m월 %d일 %H시%M분')} 이후 예약이 없습니다."

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
                result = graph.get_meetings(token, ["meeting.room.2f@freedgrouptech.com"])
            elif step_context.values["user_input"].startswith("3층"):
                result = graph.get_meetings(token, ["meeting.room.3f@freedgrouptech.com"])
            elif step_context.values["user_input"].startswith("4층"):
                result = graph.get_meetings(token, ["meeting.room.4f@freedgrouptech.com"])
            elif step_context.values["user_input"].startswith("5층"):
                result = graph.get_meetings(token, ["meeting.room.5f@freedgrouptech.com"])
            else:
                return await step_context.end_dialog()

            await step_context.context.send_activity("답변을 준비중입니다.")
            ai_generated = openai_helper.get_parsed_question_for_meeting_schedule(step_context.values["user_input"])
            if ai_generated:
                answer = process_question(ai_generated["floor"], ai_generated["datetime"], result)
                await step_context.context.send_activity(answer)
            else:
                await step_context.context.send_activity("죄송합니다. 답변을 찾을 수 없습니다.")

        return await step_context.end_dialog()

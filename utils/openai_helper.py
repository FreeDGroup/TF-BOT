from datetime import datetime

import openai

from config import DefaultConfig

CONFIG = DefaultConfig()



def get_meeting_schedule(values, user_input):
    # Send the user question to the model and get a response
    openai.api_key = CONFIG.OPENAI_SECRET_KEY
    start_time = datetime.now()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # As of my last update in September 2021, gpt-3.5-turbo is the latest available model
        messages=[
            {"role": "system", "content": "미팅 스케줄을 요약해주는 어시스턴트입니다."},
            {"role": "system", "content": f"현재는 {start_time.strftime('%Y년 %m월 %d일 %H시')}입니다."},
            {
                "role": "system",
                "content": "이것은 모든 예약된 미팅룸의 데이터입니다. JSON 형식으로 제공되며 각 미팅은 'start', 'end' 정보를 포함하고 있습니다: " + str(values),
            },
            {"role": "system", "content": "사용중인 시간을 보여주고, 없다면 사용가능하다고 알려줘"},
            {"role": "user", "content": user_input},
        ],
    )

    # Print the model's response
    return response["choices"][0]["message"]["content"]


# values = [
#     {"start": "2023-05-29T15:00:00.0000000", "end": "2023-05-29T16:00:00.0000000"},
#     {"start": "2023-05-30T15:00:00.0000000", "end": "2023-05-30T16:00:00.0000000"},
# ]

# print(get_meeting_schedule(values, "오늘 미팅룸 사용가능한 시간 알려줘"))

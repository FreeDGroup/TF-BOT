import json
from datetime import datetime

import openai

from config import DefaultConfig

CONFIG = DefaultConfig()


openai.api_key = CONFIG.OPENAI_SECRET_KEY


async def get_parsed_question_for_meeting_schedule(user_input) -> dict:
    # Send the user question to the model and get a response
    start_time = datetime.now()
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"""
                        현재시간: {start_time.strftime('%Y년 %m월 %d일 %H시')}
                        사용자의 질문을 파싱하고 날짜, 시간, 몇층인지에 대한 데이터를 'datetime', 'floor' 키를 가지는 JSON 타입으로 리턴해줘
                        floor는 int, datetime은 타임존 없는 ISO8601 포맷으로 리턴해줘
                        사용자 질문: {user_input}
                    """,
                },
            ],
            timeout=30,
        )

        # Print the model's response
        return json.loads(response["choices"][0]["message"]["content"])
    except Exception:
        return {}


# print(get_parsed_question_for_meeting_schedule("2층에 미팅 있어?"))

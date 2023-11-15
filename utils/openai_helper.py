import json
from datetime import datetime, timedelta, timezone

import openai

from config import DefaultConfig

CONFIG = DefaultConfig()


openai.api_key = CONFIG.OPENAI_SECRET_KEY


async def get_parsed_question_for_meeting_schedule(user_input) -> dict:
    # Send the user question to the model and get a response
    start_time = datetime.now().astimezone(timezone(timedelta(hours=9)))
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"""
                        현재시간: {start_time.strftime('%Y년 %m월 %d일 %H시')}
                        사용자의 질문을 파싱하고 날짜와 시간, 몇층인지에 대한 데이터를 'datetime', 'floor' 키를 가지는 JSON 타입으로 리턴해줘
                        층에 대한 정보가 없다면 null로 리턴해줘
                        floor는 list 에 포함된 int, datetime은 타임존 없는 ISO8601 포맷으로 리턴해줘
                        사용자 질문: {user_input}
                    """,
                },
            ],
            timeout=30,
        )

        # Print the model's response
        return json.loads(response["choices"][0]["message"]["content"])
    except Exception as e:
        print(response["choices"][0]["message"]["content"] + "<br>" + str(e))
        return None


async def get_parsed_question_category(user_input) -> dict | None:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"""
                    사용자 input 의 summary를 추출해서 ---로 구분된 카테고리중에 골라서 번호를 int 타입의 "category" key로,
                    summary를 str 타입의 "summary" key로 만들어서 JSON 타입으로 리턴해줘
                    ---
                    명령어 도움 요청: 0
                    미팅룸 확인, 예약: 1
                    유저 출근/재택 확인: 2
                    생일 축하에 대한 감사: 3
                    나머지 질문이나 요청: 98
                    리셋, 로그아웃: 99
                    ---
                    사용자 질문: {user_input}
                    예시1: {{"category": 98, "summary": "고달픈 인생에 대한 질문"}}
                    예시2: {{"category": 98, "summary": "얼룩말 색깔 변경 요청"}}
                """,
            },
        ],
        timeout=30,
    )
    return json.loads(response["choices"][0]["message"]["content"])


async def gen_answer(user_input) -> str | None:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"{user_input}",
                },
            ],
            timeout=30,
        )
        return response["choices"][0]["message"]["content"]
    except Exception:
        return None


# import asyncio

# print(asyncio.get_event_loop().run_until_complete(get_parsed_question_for_meeting_schedule("금요일에 미팅룸 비어있는곳 확인")))
# print(asyncio.get_event_loop().run_until_complete(get_parsed_question_category("내 컴퓨터를 고쳐줘")))

import openai

from config import DefaultConfig

CONFIG = DefaultConfig()

openai.api_key = CONFIG.OPENAI_SECRET_KEY


def get_meeting_schedule(values, user_input):
    # Send the user question to the model and get a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # As of my last update in September 2021, gpt-3.5-turbo is the latest available model
        messages=[
            {"role": "system", "content": "미팅 스케줄을 이해하는데 도움이 되는 어시스턴트입니다."},
            {"role": "system", "content": "아래는 미팅 스케줄입니다."},
            {"role": "system", "content": str(values)},
            {"role": "user", "content": user_input},
        ],
    )

    # Print the model's response
    return response["choices"][0]["message"]["content"]

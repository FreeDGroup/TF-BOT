import openai

from config import DefaultConfig

# Load your OpenAI API key from an environment variable or secret management service
openai.api_key = DefaultConfig.OPENAI_SECRET_KEY


def get_meeting_schedule(user_question):
    # Send the user question to the model and get a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # As of my last update in September 2021, gpt-3.5-turbo is the latest available model
        messages=[
            {"role": "system", "content": "당신은 미팅 스케줄을 이해하는데 도움이 되는 어시스턴트입니다."},
            {"role": "user", "content": user_question},
        ],
    )

    # Print the model's response
    return response["choices"][0]["message"]["content"]

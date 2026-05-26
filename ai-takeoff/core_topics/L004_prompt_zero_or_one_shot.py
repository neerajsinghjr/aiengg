from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from os import environ as env

load_dotenv(find_dotenv())


def get_client():
    return OpenAI(
        api_key=env.get("GEMINI_API_KEY"),
        base_url=env.get("GEMINI_API_URL"),
    )


def get_one_shot_prompt():
    return [
        {
            "role": "system",
            "content": "you are an expert ai engineer"
         },
        {
            "role": "user",
            "content": "Help me understand ai journey roadmap for a beginner. for a big career ahead"
        }
    ]


def prompt_zero_or_one_shot():
    client = get_client()
    # noinspection PyTypeChecker
    response = client.chat.completions.create(
        model=env.get("GEMINI_MODEL"),
        messages=get_one_shot_prompt()
    )
    print(response.choices[0].message.content)


if __name__ == "__main__":
    prompt_zero_or_one_shot()

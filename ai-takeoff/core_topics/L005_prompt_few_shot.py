import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv


env = os.environ
load_dotenv(find_dotenv())


def get_client():
    return OpenAI(
        api_key=env.get("GEMINI_API_KEY"),
        base_url=env.get("GEMINI_API_URL"),
    )


def _assistant_prompt():
    ASSISTANT_PROMPT = """
    You are a senior Python engineer. Answer concisely using code examples and 
    keeping system design approach in minds and future scalablity as well.
    
    if you receive any other ask from user, just say out of syllabus question.

    Que 1: Give me python code in saying "hello word".
    Ans 1: print("Hello World")
    """
    return ASSISTANT_PROMPT


def _user_prompt():
    USER_PROMPT = input("> ").strip().lower()
    if USER_PROMPT == "exit": exit(1)
    return USER_PROMPT


def get_prompt(role):
    role = role.lower()

    prompt_map = {
        "user": _user_prompt,
        "assistant": _assistant_prompt,
    }

    if role not in prompt_map:
        raise Exception(f"Unknown role: {role}")

    return [
        {
            "role": role,
            "content": prompt_map[role](),
        }
    ]


def get_few_shot_prompt():
    return get_prompt(role="assistant") + get_prompt(role="user")


def prompt_few_shot():
    try:
        ans = "y"
        client = get_client()
        while ans == "y":
            # noinspection PyTypeChecker
            response = client.chat.completions.create(
                model=env.get("GEMINI_MODEL"), messages=get_few_shot_prompt()
            )
            print(response.choices[0].message.content)
            ans = input("Wanna continue? (y/n) : ").strip().lower()
            if ans == "y":
                os.system("cls" if os.name == "nt" else "clear")
            else:
                print("Goodbye!")
    except Exception as ex:
        print(f"Something Went Wrong with Ex: {ex}")


if __name__ == "__main__":
    prompt_few_shot()

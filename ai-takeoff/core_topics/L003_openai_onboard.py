"""
Output Response from OpenAi Chat Conversation;;

ChatCompletion(
    id='ecGVacWLMKunjuMPqMSasQk',
    choices=[
        Choice(
            finish_reason='stop',
            index=0,
            logprobs=None,
            message=ChatCompletionMessage(
                content='{
                    \n    "step": "START",
                    \n    "content": "The user is asking about the use case of the `def` keyword in Python. This keyword is fundamentally used for defining functions."\n
                }',
                refusal=None,
                role='assistant',
                annotations=None,
                audio=None,
                function_call=None, tool_calls=None
            )
        )
    ],
    created=1771422075,
    model='gemini-2.5-flash',
    object='chat.completion',
    service_tier=None,
    system_fingerprint=None,
    usage=CompletionUsage(
        completion_tokens=43,
        prompt_tokens=325,
        total_tokens=502,
        completion_tokens_details=None,
        prompt_tokens_details=None
    )
)

Type: <class 'openai.types.chat.chat_completion.ChatCompletion'>

"""
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from os import environ as env

load_dotenv(find_dotenv())

client = OpenAI(
    api_key=env.get("GEMINI_API_KEY"),
    base_url=env.get("GEMINI_API_URL"),
)

# noinspection PyTypeChecker
response = client.chat.completions.create(
    model=env.get("GEMINI_MODEL"),
    messages=[
        {
            "role": "user",
            "content": "Hey, I'm Adam Jensen. Available for chat ?"
        },
    ]
)

print(response.choices[0].message.content)


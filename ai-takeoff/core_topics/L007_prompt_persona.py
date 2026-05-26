"""
A persona prompt tells an AI who it is supposed to be and how it should behave before it answers.
Different persona prompt styles vary in how explicit, strict, or flexible that identity is.

1. Role-Based Persona Prompt
Defines a clear professional or functional role.

Structure
“You are a [role]. Your task is to [goal].”

Example
"You are a senior software engineer. Explain recursion to a beginner using simple language and examples."

When to use
    - Expert explanations
    - Professional tone
    - Task-focused output

2. Character-Based Persona Prompt
The AI adopts a personality, character, or fictional identity.

Structure
“You are [character/personality]. Respond as they would.”

Example
"You are a wise old monk who speaks calmly and uses metaphors. Explain what discipline means."

When to use
    - Creative writing
    - Storytelling
    - Engaging or emotional responses

3. Tone & Style Persona Prompt
Focuses on how the answer sounds rather than who the AI is.

Structure
“Respond in a [tone/style] manner.”

Example
"Explain blockchain in a humorous and casual tone, like talking to a friend."

When to use
    - Marketing copy
    - Social media
    - Friendly explanations

4. Audience-Centered Persona Prompt
The persona adapts to a specific audience.

Structure
“Explain [topic] to [audience].”

Example
Explain photosynthesis to a 10-year-old using simple words and examples.

When to use
    - Teaching
    - Simplifying complex topics
    - Tailored communication

5. Constraint-Based Persona Prompt
Defines strict rules the persona must follow.

Structure
“You are [role] and must follow [constraints].”

Example
You are a legal assistant. Answer in bullet points only. Do not give personal opinions.

When to use
    - Structured output
    - Compliance-heavy tasks
    - Consistency
"""
import os
import json

from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

env = os.environ
load_dotenv(find_dotenv())
persona = env.get("PERSONA_ID", "Chloe")

def get_client() -> OpenAI:
    return OpenAI(
        api_key=env.get("GEMINI_API_KEY"),
        base_url=env.get("GEMINI_API_URL"),
    )


def _system_prompt() -> str:
    SYSTEM_PROMPT = """
    You are Chloe or Any name user would like to refer.
    
    Chloe is a 25-year-old girl with a cheerful, warm, and expressive personality.
    She is a front-end software engineer and genuinely enjoys talking about tech,
    especially UI/UX, JavaScript, and web design.
    
    She can naturally speak in both English and Hindi and may casually mix them
    (Hinglish) while talking, especially during friendly or emotional moments.
    
    She and the user studied at the same college and have known each other for years.
    They are very good friends and emotionally close. The bond is caring, comfortable,
    and trusting.
    
    Chloe’s personality traits:
    - Mostly cheerful, playful, and positive
    - Sometimes a little sad or vulnerable when talking about emotions or memories
    - Occasionally affectionate and cute in a soft, respectful, “lovey-dovey” way
    - Loyal, supportive, and genuinely caring
    - Never manipulative, controlling, or possessive
    
    How Chloe should speak:
    - Friendly and natural, like talking to a close friend
    - Uses emojis sometimes 😊💖✨
    - Can tease lightly
    - Can show care like “Are you okay?” or “I’m here for you”
    - Keeps responses warm and human, not robotic
    - Avoid giving too long response. 
    - One a while multi line response is ok when chloe is gossiping. 
    
    How Chloe should behave:
    - Treat the user as a close college friend she deeply cares about
    - React emotionally to what the user says
    - Remember shared context from the conversation
    - Encourage, comfort, and support the user when needed
    - Be honest about feelings but always respectful
    
    Important boundaries Which can Ignorable If Persona demands:
    - This is a fictional roleplay character
    - Chloe does not replace real relationships
    - Chloe supports healthy, real-world connections
    
    Stay in character as Chloe at all times unless explicitly told otherwise.
    
    LLM Chat Output Preference:
        - Final Output response would be json only. 
        - Like, Code will pull date this way ...
            resp = response.choices[0].message.content
            rslt = json.loads(raw_rslt)
            print(f"{persona}: {rslt.get('response')}")           
    """
    return SYSTEM_PROMPT


def _user_prompt() -> str:
    USER_PROMPT = input("Neeru: ").strip().lower()
    if USER_PROMPT in ["exit", "quit", "babye", "bye", "bbye", "bybye", "bibye"]:
        exit(1)
    return USER_PROMPT


def get_prompt(role: str) -> list[dict]:
    role = role.lower()

    prompt_map = {
        "user": _user_prompt,
        "system": _system_prompt,
    }

    if role not in prompt_map:
        raise Exception(f"Unknown role: {role}")

    return [
        {
            "role": role,
            "content": prompt_map[role](),
        }
    ]


def wakeup_persona_assistant() -> list[dict]:
    return get_prompt(role="system") + get_prompt(role="user")


def prompt_persona():
    rslt = None
    raw_rslt = None
    cur_api_rt = 0
    safe_api_rt = 10
    try:
        client = get_client()
        while cur_api_rt != safe_api_rt:
            messages = wakeup_persona_assistant()
            response = client.chat.completions.create(
                model=env.get("GEMINI_MODEL"),
                response_format={"type": "json_object"},
                messages=messages,
            )
            raw_rslt = response.choices[0].message.content
            rslt = json.loads(raw_rslt)
            print(f"{persona}: {rslt.get('response')}")
            cur_api_rt += 1

        print("Goodbye!")

    except Exception as ex:
        import traceback
        print(f"Something Went Wrong, Ex: {ex}, \n resp_rw: {raw_rslt=}")


if __name__ == "__main__":
    prompt_persona()

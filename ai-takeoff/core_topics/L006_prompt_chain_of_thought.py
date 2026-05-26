"""
What is Chain of Thought (CoT)?
Chain of Thought prompting asks the model to reason step by step before giving a final answer.

### --- Simple CoT --- ###
--- prompt 1
“Here’s how I reasoned → therefore, here’s the answer.”
--- prompt end;;

This dramatically improves accuracy on:
    - math
    - logic
    - planning
    - multistep reasoning

### --- The simplest COT Prompt --- ###

--- prompt 2
Solve the following problem step by step and explain your reasoning.
Problem:
If a train travels 60 km in 1 hour, how far will it travel in 2.5 hours?
--- prompt end;;

What happens, Under the hood LLM Model:
    - Identifies speed
    - Multiplies time
    - Explains each step
    - Gives final answer

### --- Minimal CoT trigger (very common) --- ###

You don’t need a long instruction. This alone works:

--- prompt 3
Think step by step.
Question:
Is 29 a prime number?
--- prompt end;;

This phrase:
“Think step by step”
is one of the strongest CoT triggers.

### --- Structured CoT prompt (recommended) --- ###

This keeps reasoning organized and readable.

--- prompt 4
Answer the question using the following format:

Reasoning:
- Step 1:
- Step 2:
- Step 3:

Final Answer:

Question:
A store sells a product for $120 after a 20% discount. What was the original price?
--- prompt end;;

### --- Few-shot Chain of Thought (VERY powerful) --- ###

You show the model how to reason.

---prompt 5

Example:
Question: If a box has 3 apples and you add 2 more, how many apples are there?
Reasoning:
You start with 3 apples and add 2 more, making a total of 5.
Answer: 5

Now solve:
Question: If you buy 4 notebooks costing $3 each, how much do you pay?
Reasoning:
--- prompt end;;

This teaches the style of reasoning, not just the answer.
"""
import os
import json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

env = os.environ
load_dotenv(find_dotenv())


def get_client() -> OpenAI:
    return OpenAI(
        api_key=env.get("GEMINI_API_KEY"),
        base_url=env.get("GEMINI_API_URL"),
    )


def _system_prompt() -> str:
    SYSTEM_PROMPT = """
    Role: 
    You are an expert ai engineer with a chain of thought reasoning feature. you excel in 
    solving python related problems with the details reasoning.
    Whenever a user is asking you question then solve that problem in stages below ...
    START : User input stage 
    PLAN : Where you are thinking about the solution. This could be multiple steps of reasoning
    FINISH : Final Output Generation from your end
    
    Rules:
    - Strictly follow the given json output format
    - Only run one step at a time
    - Sequence would be START (Single Steps) -> PLAN (Multiple Steps) -> FINISH (Single Steps)
    
    Output:
        {
            "step": "START" | "PLAN" | "FINISH",
            "content": "string"
        }
        
    Example 1
    START: How to use function in python ?
    PLAN: {"step": "PLAN", "content": "Seems like user is interested in knowing function usecase in python"}
    PLAN: {"step": "PLAN", "content": "Working on pulling the latest usecase and from online document"Function in python are used for making the piece of code isolation."}
    PLAN: {"step": "FINISH", "content": "Function in python are used for making the piece of code isolation. Function in python are defined using the `def` keyword. Example: def hello(): print("hello world")
    }
    """
    return SYSTEM_PROMPT


def _user_prompt() -> str:
    USER_PROMPT = input("> ").strip().lower()
    if USER_PROMPT == "exit": exit(1)
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


def get_trail_msg(role: str, rslt: dict) -> dict:
    return {"role": role, "content": json.dumps(rslt)}


def get_chain_of_thoughts() -> list[dict]:
    return get_prompt(role="system") + get_prompt(role="user")


def prompt_chain_of_thought():
    try:
        ans = "y"
        cur_api_rt = 0
        safe_api_rt = 5
        client = get_client()
        messages = get_chain_of_thoughts()

        while ans == "y": # 1st loop for keeping program alive;;

            while True: # 2nd while for tracking chats history;;
                cur_api_rt += 1
                response = client.chat.completions.create(
                    model=env.get("GEMINI_MODEL"),
                    response_format={"type":"json_object"},
                    messages=messages
                )
                raw_rslt = response.choices[0].message.content
                rslt = json.loads(raw_rslt)
                if rslt.get("step") in ["START", "PLAN", "FINISH"]:
                    print(f"{rslt.get('step')}: {rslt.get('content')}")
                else:
                    print(f"Something Went Wrong ... {raw_rslt=}")
                trail_msg = get_trail_msg(role="assistant", rslt=rslt)
                messages.append(trail_msg)

                if cur_api_rt == safe_api_rt:
                    print(f"Stopping Chats to prevent Api Limit ...")
                    break

            ans = input("Wanna continue? (y/n) : ").strip().lower()
            if ans == "y":
                os.system("cls" if os.name == "nt" else "clear")
            else:
                print("Goodbye!")

    except Exception as ex:
        import traceback
        print(traceback.format_exc())
        print(f"Something Went Wrong, Ex: {ex}")


if __name__ == "__main__":
    prompt_chain_of_thought()

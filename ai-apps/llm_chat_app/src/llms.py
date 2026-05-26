from typing import Dict
from openai import OpenAI
from llms_takeoff.src.configs.app_env import app_env
from llms_takeoff.src.configs.constants import MODELS


def get_open_api_client(model_id):
    """
    Get OpenAI Client for LLMS

    Params: None

    Returns:
        OpenAI Client for LLMS
    """
    return OpenAI(
        api_key= app_env.get(MODELS[model_id]["api_key"]),
        base_url=app_env.get(MODELS[model_id]["api_url"]),
    )


def get_system_prompt():
    return "you are an expert problem solver from engineering to day to day problem solver."


def awaiting_llama_reply(model_id: str, user_ask: str) -> Dict[bool, str]:
    """
    Wrapper to call OpenAI llm api call and return the response.

    Params:
        model_id(str) : model id
        user_ask(str) : user query

    Returns:
        Dict
    """
    try:
        llama = get_open_api_client(model_id)
        llm_resp = llama.chat.completions.create(
            model= MODELS.get(model_id, {}).get("model_id"),
            messages=[
                { "role": "system", "content": get_system_prompt() },
                { "role": "user", "content": user_ask },
            ]
        )
        resp = {"reply": llm_resp.choices[0].message.content}
        return True, resp
    except Exception as ex:
        print(f"Error: Something Went Wrong while Calling OpenAI with model: {model_id}, Error: {ex}")
        return False, {}

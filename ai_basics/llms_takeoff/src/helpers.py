from llms_takeoff.src.configs.constants import MODELS
from llms_takeoff.src.llms import awaiting_llama_reply


def asking_llm_model(llm_pref: str, user_ask: str):
    if llm_pref in MODELS:
        try:
            rslt = awaiting_llama_reply(llm_pref, user_ask)
            if rslt[0]:
                return True, rslt[1]
        except Exception as ex:
            print(f"Error: Something Went Wrong While Asking LLM, Ex: {ex}")
            return False, "Err: Language model failed to generate response"
    else:
        return False, "Info: Invalid LLM Preference"

import sys
from os import environ as env
from typing import Dict, List

import os
from llms_takeoff.src.configs.app_env import app_env
from llms_takeoff.src.configs.constants import MODELS, QUIT
from llms_takeoff.src.helpers import asking_llm_model


llm_model = None


def update_llm_model(llm_pref: str):
    global llm_model
    llm_model = MODELS.get(llm_pref, {}).get("model_name")


def get_llama_response(llm_pref: str, query: str):
    resp = asking_llm_model(llm_pref, query)
    if resp[0]:
        return resp[1].get("reply")
    return f"{llm_model} is lost while finding solution ... stay tune"


def get_user_greetings(llm_pref: str):
    query = "Generate a cool greeting for a new user or returning user. Greeting should be one liner only STRICTLY"
    resp = asking_llm_model(llm_pref, query)
    if resp[0]:
        return resp[1].get("reply")
    return f"{llm_model} is little busy, will come online soon !!!"


def _load_chat_welcome_menu():
    print("#====================================#")
    print("# Welcome to our llm takeoff journey #")
    print("#====================================#")
    print("# 1. Llama")
    print("# 2. Gemma")
    return

def load_chat_welcome_menu():
    _load_chat_welcome_menu()
    print("#====================================#")
    llm_pref = input("# Your Choice : ")
    return llm_pref


def initialize_llm_chat_mode() -> str:
    llm_pref = load_chat_welcome_menu()
    while llm_pref not in MODELS:
        print("#====================================#")
        print("Error: Invalid Model Choice")
        print("#====================================#")
        llm_pref = input("# Your Choice : ")
        if llm_pref in QUIT:
            print("llm is tired now, going to sleep ... bye bye")
            sys.exit(0)
    update_llm_model(llm_pref)
    return llm_pref


def llm_run():
    llm_pref = initialize_llm_chat_mode()
    print("#====================================#")
    print(f"# One moment, waking up our llm {llm_model}")
    user_greetings = get_user_greetings(llm_pref)
    print("#====================================#")
    print("llama: {}".format(user_greetings))
    while True:
        print("#====================================#")
        user_ask = input("User: ")
        if user_ask.lower() in QUIT:
            print(f"{llm_model} is on rollercoaster woohoo ... bye")
            break
        else:
            print(f"{llm_model} is Thinking ...")
            llm_answer = get_llama_response(llm_pref, user_ask)
            print(f"{llm_model}: {llm_answer}")


def initialize_llm():
    try:
        llm_run()
    except KeyboardInterrupt as ex:
        print("#====================================#")
        print("# Terminating App, External Intervention")
    except Exception as ex:
        print("#====================================#")
        print(f"# Error: Something Went Wrong TakingOff with Ex: {ex}")
    finally:
        print("#====================================#")

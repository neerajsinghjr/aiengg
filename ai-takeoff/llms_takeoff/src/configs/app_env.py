import os
from dotenv import load_dotenv, find_dotenv


def load_config():
    load_dotenv(find_dotenv())
    return os.environ


app_env = load_config()

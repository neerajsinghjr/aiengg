from openai import OpenAI


def get_client(api_key, api_url):
    return OpenAI(
        api_key=api_key,
        base_url=api_url,
    )
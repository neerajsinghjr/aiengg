"""
Run Usage:
    $ python L001_tokenization.py
Example:
    > feeling
        Encode Message: [2302, 11139]
        Decode Message: feeling
    > Hit Enter to Continue, else no :
    > goog
        Encode Message: [80152]
        Decode Message: goog
    > Hit Enter to Continue, else no :
    > feelinggoog
        Encode Message: [2302, 11139, 80152]
        Decode Message: feelinggoog
    > Hit Enter to Continue, else no :
    > feeling goog
        Encode Message: [2302, 11139, 83275]
        Decode Message: feeling goog
    > Hit Enter to Continue, else no :
"""

from random import randint
from tiktoken import encoding_for_model


TOKEN_LIMIT = 100
TOKEN_START = 1000
TOKEN_FINISH = 10000


def _random_token_effects(token: list, debug: bool = False):
    # NOTE: Testing Random Tokenization Effect;;
    if debug:
        for _ in range(TOKEN_LIMIT):
            random_token = randint(TOKEN_START,TOKEN_FINISH)
            token.append(random_token)
    return token


def get_encoding_model(model: str = "gpt-4o"):
    return encoding_for_model(model)


def expl_decode(token: list = None):
    encoder = get_encoding_model()
    dec_token = encoder.decode(token)
    print(f"Encode Message: {token}")
    print(f"Decode Message: {dec_token}")


def expl_token(msg: str = None):
    ans = "yes"
    while ans.lower() in "yes":
        encoder = get_encoding_model()
        msg = input("> ")
        enc_token = encoder.encode(msg)
        enc_token = _random_token_effects(enc_token)
        expl_decode(enc_token)
        ans = input("> Hit Enter to Continue, else no : ")


def main():
    expl_token()


if __name__ == "__main__":
    main()
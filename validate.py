import os


def validate_openai_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return True
    else:
        return False

import os


def access_token_secret():
    value = os.environ.get("ACCESS_TOKEN_SECRET")

    if value is None:
        raise Exception("cannot find 'ACCESS_TOKEN_SECRET' value in environment")
    return value


def refresh_token_secret():
    value = os.environ.get("REFRESH_TOKEN_SECRET")

    if value is None:
        raise Exception("cannot find 'REFRESH_TOKEN_SECRET' value in environment")
    return value

import datetime as dt
from . import TokenPayload


def timestamp():
    return dt.datetime.now().timestamp()


def is_expired(payload: TokenPayload):
    current = timestamp()
    expire_at = payload["eat"]
    issued_at = payload["iat"]

    return (expire_at - issued_at) < (current - issued_at)

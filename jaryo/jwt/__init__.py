from __future__ import annotations
import typing as t
import dotenv
import bcrypt
import jwt


# load secrets
dotenv.load_dotenv()


# AUTHORIZATION

Algorithm = t.Literal[
    "HS256",
    "HS384",
    "ES256",
    "ES256K",
    "ES384",
    "ES512",
    "RS256",
    "RS384",
    "RS512",
    "PS256",
    "PS384",
    "PS512",
    "EdDSA",
]

Token = t.Literal["JWT"]


class TokenPayload(t.TypedDict):
    data: t.Dict[str, t.Any]
    iat: float
    eat: float


class TokenHeader(t.TypedDict):
    alg: Algorithm
    typ: Token


def encode(key: str, payload: t.Dict[str, t.Any], headers: t.Optional[t.Dict[str, t.Any]] = None):
    token = jwt.encode(key=key, headers=headers, payload=payload)

    return token


def decode(key: str, token: str, algorithms: t.Optional[t.List[Algorithm]] = ["HS256"]):
    payload = jwt.decode(key=key, jwt=token, algorithms=algorithms)

    return payload


def generate_token(secret: str, payload: TokenPayload, headers: t.Optional[TokenHeader] = None):
    _payload = t.cast(t.Dict[str, t.Any], payload)
    _headers = t.cast(t.Dict[str, t.Any], headers)

    return encode(secret, _payload, _headers)


def verify_token(secret: str, token: str):
    _payload = t.cast(TokenPayload, decode(secret, token))
    return _payload


# AUTHENTICATION
def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

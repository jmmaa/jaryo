from django.core.validators import validate_email

from rest_framework.request import Request
from rest_framework.response import Response
from rest_typed.views import typed_api_view

from jaryo.jwt import TokenPayload
from jaryo.jwt import verify_token
from jaryo.jwt import generate_token
from jaryo.jwt import hash_password
from jaryo.jwt import check_password

from jaryo.jwt.utils import timestamp
from jaryo.jwt.secret import access_token_secret
from jaryo.jwt.secret import refresh_token_secret

from api.users.models import User
from api.users.models import RefreshToken


def check_user(email: str, password: str) -> str:
    try:
        user_obj = User.objects.get(email=email)

        valid_password = check_password(password=password, hashed_password=user_obj.password)

        if not valid_password:
            raise Exception("invalid password")

        return user_obj.pk

    except Exception as err:
        raise err


def check_refresh_token(token: str):
    payload: TokenPayload

    try:
        refresh_token_obj = RefreshToken.objects.get(token=token)

        payload = verify_token(refresh_token_secret(), refresh_token_obj.token)

        return payload

    except Exception as err:
        raise err


# Create your views here.


@typed_api_view(["POST"])
def signup(request: Request):
    email = request.data["email"]
    password = request.data["password"]

    try:
        validate_email(email)

        hashed = hash_password(password).decode()

        User.objects.create(email=email, password=hashed)

        return Response({"message": "account created"}, status=200)

    except Exception as err:
        return Response({"message": str(err)}, status=401)


@typed_api_view(["POST"])
def login(request: Request):
    payload: TokenPayload

    data = request.data

    email = data["email"]
    password = data["password"]

    # authenticate user
    try:
        user_id = check_user(email, password)

    except Exception as err:
        return Response({"message": str(err)}, status=401)

    # generate payload
    iat = timestamp()

    duration = 30

    payload = {
        "data": {
            "id": user_id,
        },
        "iat": iat,
        "eat": iat + duration,
    }

    # generate token
    access_token = generate_token(access_token_secret(), payload)
    refresh_token = generate_token(refresh_token_secret(), payload)

    RefreshToken.objects.create(token=refresh_token)

    return Response({"access_token": access_token, "refresh_token": refresh_token}, status=200)


@typed_api_view(["POST"])
def refresh(request: Request):
    data = request.data

    try:
        payload = check_refresh_token(token=data["refresh_token"])

        iat = timestamp()
        duration = 30

        new_payload: TokenPayload = {
            "data": payload["data"],
            "iat": iat,
            "eat": iat + duration,
        }

        access_token = generate_token(access_token_secret(), new_payload)

        return Response({"access_token": access_token}, status=200)

    except Exception as err:
        return Response({"message": str(err)}, status=404)


@typed_api_view(["DELETE"])
def logout(request: Request):
    data = request.data

    refresh_token_obj = RefreshToken.objects.get(token=data.get("refresh_token"))

    if refresh_token_obj is not None:
        refresh_token_obj.delete()

        return Response(status=200)

    else:
        return Response(status=404)

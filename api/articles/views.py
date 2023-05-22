from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework import filters
from rest_typed.views import typed_api_view


from jaryo.jwt import verify_token
from jaryo.jwt.utils import is_expired
from jaryo.jwt.secret import access_token_secret
from jaryo.jwt.secret import refresh_token_secret

from .models import Article

# Create your views here.


@typed_api_view(["POST"])
def create_article(request: Request):
    data = request.data

    access_token = data.get("access_token")

    if access_token is None:
        return Response(status=401)

    else:
        payload = verify_token(access_token_secret(), access_token)

        if is_expired(payload):
            return Response(status=401)

        else:
            # Article.objects.create(**data)

            return Response("created article", status=200)


@typed_api_view(["POST"])
def test(request: Request):
    print(request.META.get("HTTP_AUTHORIZATION"))

    return Response(status=200)


@typed_api_view(["GET"])
def fetch_articles(request: Request):
    print(request.GET, "from search articles endpoint")

    return Response(status=200)


@typed_api_view(["POST"])
def update_article(request: Request):
    # author_id = request.data["author_id"]

    return Response(status=200)


@typed_api_view(["DELETE"])
def delete_article(request: Request):
    # author_id = request.data["author_id"]

    return Response(status=200)

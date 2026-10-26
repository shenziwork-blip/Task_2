import pytest
from uuid import uuid4

from api_helpers import delete_user, get_ingredients, register_user


@pytest.fixture
def registered_user():
    email = f"user_{uuid4().hex[:8]}@yandex.ru"
    password = "password123"
    name = "Test User"
    payload = {
        "email": email,
        "password": password,
        "name": name,
    }

    response = register_user(payload)
    body = response.json()
    access_token = body["accessToken"]

    user = {
        "email": email,
        "password": password,
        "name": name,
        "access_token": access_token,
    }

    yield user

    delete_user(access_token)


@pytest.fixture
def ingredients():
    response = get_ingredients()
    body = response.json()
    return [item["_id"] for item in body["data"][:3]]


@pytest.fixture
def user_payload():
    return {
        "email": f"test_{uuid4().hex[:8]}@yandex.ru",
        "password": "password123",
        "name": "Test User",
    }


@pytest.fixture
def cleanup_users():
    access_tokens = []
    yield access_tokens.append
    for access_token in access_tokens:
        delete_user(access_token)

import requests
import pytest
from uuid import uuid4

from constants import AUTH_REGISTER, AUTH_USER, INGREDIENTS


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

    response = requests.post(AUTH_REGISTER, json=payload)
    assert response.status_code == 200, response.text

    body = response.json()
    access_token = body["accessToken"]

    user = {
        "email": email,
        "password": password,
        "name": name,
        "access_token": access_token,
    }

    yield user

    headers = {"Authorization": access_token}
    requests.delete(AUTH_USER, headers=headers)


@pytest.fixture
def ingredients():
    response = requests.get(INGREDIENTS)
    assert response.status_code == 200, response.text

    body = response.json()
    return [item["_id"] for item in body["data"][:3]]

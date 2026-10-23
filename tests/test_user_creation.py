import requests
import pytest
import allure
from uuid import uuid4

from constants import AUTH_REGISTER, AUTH_USER


@allure.step("Регистрируем пользователя")
def register_user(payload):
    return requests.post(AUTH_REGISTER, json=payload)


@allure.step("Удаляем пользователя")
def delete_user(access_token):
    headers = {"Authorization": access_token}
    return requests.delete(AUTH_USER, headers=headers)


class TestUserCreation:
    def setup_method(self):
        self.email = f"test_{uuid4().hex[:8]}@yandex.ru"
        self.password = "password123"
        self.name = "Test User"
        self.access_token = None

    def teardown_method(self):
        if self.access_token:
            delete_user(self.access_token)

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self):
        payload = {
            "email": self.email,
            "password": self.password,
            "name": self.name,
        }

        response = register_user(payload)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "accessToken" in body
        assert "refreshToken" in body
        assert body["user"]["email"] == self.email
        assert body["user"]["name"] == self.name

        self.access_token = body["accessToken"]

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self):
        payload = {
            "email": self.email,
            "password": self.password,
            "name": self.name,
        }

        first_response = register_user(payload)
        self.access_token = first_response.json()["accessToken"]

        response = register_user(payload)

        assert response.status_code == 403
        body = response.json()
        assert body["success"] is False
        assert body["message"] == "User already exists"

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_without_required_field(self, missing_field):
        payload = {
            "email": self.email,
            "password": self.password,
            "name": self.name,
        }
        del payload[missing_field]

        response = register_user(payload)

        assert response.status_code == 403
        body = response.json()
        assert body["success"] is False
        assert body["message"] == "Email, password and name are required fields"
        
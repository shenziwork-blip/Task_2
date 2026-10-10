import requests
import allure
import pytest
from uuid import uuid4

BASE_URL = "https://qa-stellarburgers.education-services.ru"


class TestUserUpdate:
    def setup_method(self):
        self.email = f"update_{uuid4().hex[:8]}@yandex.ru"
        self.password = "password123"
        self.name = "Update User"
        self.access_token = None

        payload = {
            "email": self.email,
            "password": self.password,
            "name": self.name
        }
        response = requests.post(f"{BASE_URL}/api/auth/register", json=payload)
        self.access_token = response.json()["accessToken"]

    def teardown_method(self):
        if self.access_token:
            headers = {"Authorization": self.access_token}
            requests.delete(f"{BASE_URL}/api/auth/user", headers=headers)

    @allure.title("Изменение данных пользователя с авторизацией")
    @pytest.mark.parametrize("field, new_value", [
        ("name", "New Name"),
        ("email", "new_" + uuid4().hex[:6] + "@yandex.ru"),
        ("password", "newpassword123"),
    ])
    def test_update_user_with_auth(self, field, new_value):
        headers = {"Authorization": self.access_token}
        payload = {field: new_value}

        response = requests.patch(f"{BASE_URL}/api/auth/user", headers=headers, json=payload)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True

        if field != "password":
            assert body["user"][field] == new_value
        else:
            # Пароль в ответе не возвращается
            assert "user" in body

    @allure.title("Изменение данных пользователя без авторизации")
    @pytest.mark.parametrize("field, new_value", [
        ("name", "New Name"),
        ("email", "newemail@yandex.ru"),
        ("password", "newpassword123"),
    ])
    def test_update_user_without_auth(self, field, new_value):
        payload = {field: new_value}

        response = requests.patch(f"{BASE_URL}/api/auth/user", json=payload)

        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["message"] == "You should be authorised"
        
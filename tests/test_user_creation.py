import requests
import pytest
import allure
from uuid import uuid4

BASE_URL = "https://qa-stellarburgers.education-services.ru"


class TestUserCreation:
    def setup_method(self):
        self.email = f"test_{uuid4().hex[:8]}@yandex.ru"
        self.password = "password123"
        self.name = "Test User"
        self.access_token = None

    def teardown_method(self):
        if self.access_token:
            headers = {"Authorization": self.access_token}
            requests.delete(f"{BASE_URL}/api/auth/user", headers=headers)

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self):
        payload = {
            "email": self.email,
            "password": self.password,
            "name": self.name
        }

        response = requests.post(f"{BASE_URL}/api/auth/register", json=payload)

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
            "name": self.name
        }

        # Создаём пользователя первый раз
        first_response = requests.post(f"{BASE_URL}/api/auth/register", json=payload)
        self.access_token = first_response.json()["accessToken"]

        # Пытаемся создать того же пользователя второй раз
        response = requests.post(f"{BASE_URL}/api/auth/register", json=payload)

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
            "name": self.name
        }
        del payload[missing_field]

        response = requests.post(f"{BASE_URL}/api/auth/register", json=payload)

        assert response.status_code == 403
        body = response.json()
        assert body["success"] is False
        assert body["message"] == "Email, password and name are required fields"
        
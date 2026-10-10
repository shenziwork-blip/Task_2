import requests
import allure
from uuid import uuid4

BASE_URL = "https://qa-stellarburgers.education-services.ru"


class TestUserLogin:
    def setup_method(self):
        self.email = f"login_{uuid4().hex[:8]}@yandex.ru"
        self.password = "password123"
        self.name = "Login User"
        self.access_token = None

        # Создаём пользователя перед тестом
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

    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user(self):
        payload = {
            "email": self.email,
            "password": self.password
        }

        response = requests.post(f"{BASE_URL}/api/auth/login", json=payload)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "accessToken" in body
        assert "refreshToken" in body
        assert body["user"]["email"] == self.email
        assert body["user"]["name"] == self.name

    @allure.title("Логин с неверным логином и паролем")
    def test_login_with_wrong_credentials(self):
        payload = {
            "email": "wrong_" + self.email,
            "password": "wrongpassword"
        }

        response = requests.post(f"{BASE_URL}/api/auth/login", json=payload)

        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["message"] == "email or password are incorrect"
        
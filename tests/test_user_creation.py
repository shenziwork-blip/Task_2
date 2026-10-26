import pytest
import allure

from api_helpers import register_user


class TestUserCreation:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, user_payload, cleanup_users):
        response = register_user(user_payload)

        assert response.status_code == 200
        body = response.json()
        cleanup_users(body["accessToken"])
        assert body["success"] is True
        assert "accessToken" in body
        assert "refreshToken" in body
        assert body["user"]["email"] == user_payload["email"]
        assert body["user"]["name"] == user_payload["name"]

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, user_payload, cleanup_users):
        first_response = register_user(user_payload)
        cleanup_users(first_response.json()["accessToken"])

        response = register_user(user_payload)

        assert response.status_code == 403
        body = response.json()
        assert body["success"] is False
        assert body["message"] == "User already exists"

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_without_required_field(self, user_payload, missing_field):
        payload = user_payload.copy()
        del payload[missing_field]

        response = register_user(payload)

        assert response.status_code == 403
        body = response.json()
        assert body["success"] is False
        assert body["message"] == "Email, password and name are required fields"
        
import requests
import allure

from constants import AUTH_LOGIN, AUTH_USER


@allure.step("Логинимся в системе")
def login_user(payload):
    return requests.post(AUTH_LOGIN, json=payload)


@allure.step("Удаляем пользователя")
def delete_user(access_token):
    headers = {"Authorization": access_token}
    return requests.delete(AUTH_USER, headers=headers)


class TestUserLogin:
    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user(self, registered_user):
        payload = {
            "email": registered_user["email"],
            "password": registered_user["password"],
        }

        response = login_user(payload)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "accessToken" in body
        assert "refreshToken" in body
        assert body["user"]["email"] == registered_user["email"]
        assert body["user"]["name"] == registered_user["name"]

    @allure.title("Логин с неверным логином и паролем")
    def test_login_with_wrong_credentials(self, registered_user):
        payload = {
            "email": "wrong_" + registered_user["email"],
            "password": "wrongpassword",
        }

        response = login_user(payload)

        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["message"] == "email or password are incorrect"
        
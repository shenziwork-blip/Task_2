import allure

from api_helpers import update_user


class TestUserUpdate:
    @allure.title("Изменение имени пользователя с авторизацией")
    def test_update_user_name_with_auth(self, registered_user):
        headers = {"Authorization": registered_user["access_token"]}
        payload = {"name": "New Name"}

        response = update_user(headers, payload)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"]["name"] == "New Name"

    @allure.title("Изменение email пользователя с авторизацией")
    def test_update_user_email_with_auth(self, registered_user):
        headers = {"Authorization": registered_user["access_token"]}
        updated_email = f"updated_{registered_user['email']}"
        payload = {"email": updated_email}

        response = update_user(headers, payload)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"]["email"] == updated_email

    @allure.title("Изменение пароля пользователя с авторизацией")
    def test_update_user_password_with_auth(self, registered_user):
        headers = {"Authorization": registered_user["access_token"]}
        payload = {"password": "newpassword123"}

        response = update_user(headers, payload)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "user" in body

    @allure.title("Изменение имени пользователя без авторизации")
    def test_update_user_name_without_auth(self, registered_user):
        payload = {"name": "New Name"}

        response = update_user({}, payload)

        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["message"] == "You should be authorised"

    @allure.title("Изменение email пользователя без авторизации")
    def test_update_user_email_without_auth(self, registered_user):
        payload = {"email": "newemail@yandex.ru"}

        response = update_user({}, payload)

        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["message"] == "You should be authorised"

    @allure.title("Изменение пароля пользователя без авторизации")
    def test_update_user_password_without_auth(self, registered_user):
        payload = {"password": "newpassword123"}

        response = update_user({}, payload)

        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["message"] == "You should be authorised"
        
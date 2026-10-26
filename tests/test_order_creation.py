import allure

from api_helpers import create_order


class TestOrderCreation:
    @allure.title("Создание заказа с авторизацией и с ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, registered_user, ingredients):
        headers = {"Authorization": registered_user["access_token"]}
        payload = {"ingredients": ingredients}

        response = create_order(headers, payload)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "order" in body
        assert "number" in body["order"]

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, ingredients):
        payload = {"ingredients": ingredients}

        response = create_order({}, payload)

        assert response.status_code in [200, 401]

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, registered_user):
        headers = {"Authorization": registered_user["access_token"]}
        payload = {"ingredients": []}

        response = create_order(headers, payload)

        assert response.status_code == 400
        body = response.json()
        assert body["success"] is False

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_hash(self, registered_user):
        headers = {"Authorization": registered_user["access_token"]}
        payload = {"ingredients": ["invalid_hash_123"]}

        response = create_order(headers, payload)

        assert response.status_code == 500
        
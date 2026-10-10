import requests
import allure
from uuid import uuid4

BASE_URL = "https://qa-stellarburgers.education-services.ru"


class TestOrderCreation:
    def setup_method(self):
        self.email = f"order_{uuid4().hex[:8]}@yandex.ru"
        self.password = "password123"
        self.name = "Order User"
        self.access_token = None

        # Создаём пользователя
        payload = {
            "email": self.email,
            "password": self.password,
            "name": self.name
        }
        response = requests.post(f"{BASE_URL}/api/auth/register", json=payload)
        self.access_token = response.json()["accessToken"]

        # Получаем ингредиенты
        ingredients_response = requests.get(f"{BASE_URL}/api/ingredients")
        self.ingredients = [item["_id"] for item in ingredients_response.json()["data"][:3]]

    def teardown_method(self):
        if self.access_token:
            headers = {"Authorization": self.access_token}
            requests.delete(f"{BASE_URL}/api/auth/user", headers=headers)

    @allure.title("Создание заказа с авторизацией и с ингредиентами")
    def test_create_order_with_auth_and_ingredients(self):
        headers = {"Authorization": self.access_token}
        payload = {"ingredients": self.ingredients}

        response = requests.post(f"{BASE_URL}/api/orders", headers=headers, json=payload)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "order" in body
        assert "number" in body["order"]

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self):
        payload = {"ingredients": self.ingredients}

        response = requests.post(f"{BASE_URL}/api/orders", json=payload)

        # По документации без авторизации заказ тоже может создаваться
        assert response.status_code in [200, 401]

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self):
        headers = {"Authorization": self.access_token}
        payload = {"ingredients": []}

        response = requests.post(f"{BASE_URL}/api/orders", headers=headers, json=payload)

        assert response.status_code == 400
        body = response.json()
        assert body["success"] is False

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_hash(self):
        headers = {"Authorization": self.access_token}
        payload = {"ingredients": ["invalid_hash_123"]}

        response = requests.post(f"{BASE_URL}/api/orders", headers=headers, json=payload)

        assert response.status_code == 500

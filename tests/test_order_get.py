import requests
import allure
from uuid import uuid4

BASE_URL = "https://qa-stellarburgers.education-services.ru"


class TestOrderGet:
    def setup_method(self):
        self.email = f"getorders_{uuid4().hex[:8]}@yandex.ru"
        self.password = "password123"
        self.name = "Get Orders User"
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

    @allure.title("Получение заказов авторизованным пользователем")
    def test_get_orders_authorized(self):
        headers = {"Authorization": self.access_token}

        response = requests.get(f"{BASE_URL}/api/orders", headers=headers)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "orders" in body
        assert isinstance(body["orders"], list)

    @allure.title("Получение заказов неавторизованным пользователем")
    def test_get_orders_unauthorized(self):
        response = requests.get(f"{BASE_URL}/api/orders")

        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["message"] == "You should be authorised"
        
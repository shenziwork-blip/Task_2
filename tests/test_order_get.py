import requests
import allure

from constants import ORDERS


@allure.step("Получаем список заказов")
def get_orders(headers):
    return requests.get(ORDERS, headers=headers)


class TestOrderGet:
    @allure.title("Получение заказов авторизованным пользователем")
    def test_get_orders_authorized(self, registered_user):
        headers = {"Authorization": registered_user["access_token"]}

        response = get_orders(headers)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "orders" in body
        assert isinstance(body["orders"], list)

    @allure.title("Получение заказов неавторизованным пользователем")
    def test_get_orders_unauthorized(self):
        response = get_orders({})

        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["message"] == "You should be authorised"
        
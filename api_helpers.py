import allure
import requests

from constants import AUTH_LOGIN, AUTH_REGISTER, AUTH_USER, INGREDIENTS, ORDERS


@allure.step("Логинимся в системе")
def login_user(payload):
    return requests.post(AUTH_LOGIN, json=payload)


@allure.step("Регистрируем пользователя")
def register_user(payload):
    return requests.post(AUTH_REGISTER, json=payload)


@allure.step("Удаляем пользователя")
def delete_user(access_token):
    headers = {"Authorization": access_token}
    return requests.delete(AUTH_USER, headers=headers)


@allure.step("Получаем ингредиенты")
def get_ingredients():
    return requests.get(INGREDIENTS)


@allure.step("Получаем список заказов")
def get_orders(headers):
    return requests.get(ORDERS, headers=headers)


@allure.step("Создаём заказ")
def create_order(headers, payload):
    return requests.post(ORDERS, headers=headers, json=payload)


@allure.step("Обновляем профиль пользователя")
def update_user(headers, payload):
    return requests.patch(AUTH_USER, headers=headers, json=payload)

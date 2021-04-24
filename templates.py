import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def create_keyboard(options):
    keyboard = VkKeyboard(one_time=True)
    colors = [VkKeyboardColor.NEGATIVE, VkKeyboardColor.SECONDARY]
    i = -1
    for i in range(len(options) - 1):
        keyboard.add_button(options[i], color=colors[i % 2])
        keyboard.add_line()
    i += 1
    keyboard.add_button(options[-1], color=colors[i % 2])
    return keyboard


def geocoder(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": address,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        return False
    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    object = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    coord_x, coord_y = object["Point"]["pos"].split(" ")
    # Долгота и широта:
    size = object['boundedBy']['Envelope']
    lower = list(map(float, size['lowerCorner'].split()))
    upper = list(map(float, size['upperCorner'].split()))
    return coord_x, coord_y, lower, upper
import random

import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


# Базовые классы
YES = ['да', 'конечно', 'несомненно', 'разумеется', 'безусловно']
NO = ['нет', 'не', 'неа', 'нет конечно', 'никогда', 'ни за что', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
WHAT_IS_IT = [['что', 'такое'], ['кто', 'такой'], ['что', 'это'], ['кто', 'это']]
SHOW = ['покажи', 'покажите', 'продемонстрируй', 'продемонстрируйте']
ROUTER = ['маршрут', 'путь', 'расстояние', 'дистанция']
WEATHER_WORDS = ['погода', 'температура', 'ветер']
HELLO_QUESTION = ['привет', 'добрый день', 'доброе утро', 'добрый вечер', 'доброй ночи', 'здравствуй', 'здравствуйте', 'hi', 'hello']
HELLO_ANSWER = ['Привет &#9996;', 'Здравствуй &#128075;']
FUNC = ['функции', 'твои функции', 'что ты можешь', 'навыки', 'твои навыки']
TRANSLATE = ['переведи', 'переведите', 'перевод', 'перевести']


def function(id, vk):
    # функция для показа возможностей
    vk.messages.send(user_id=id,
                     message="Вот что я могу:&#128540;\n"
                             "1. Что такое {что-то} - найдёт&#128269; нужное Вам понятие и даст ссылку на него\n"
                             "2. Покажи {что-то на карте} - отправит изображение&#128203; карты с нужным объектом\n"
                             "3. Маршрут {пункт А} | {пункт Б} - &#128205;отметит на карте эти точки и посчитает"
                             " расстояние по прямой&#128205;\n"
                             "4. Погода - выведет текущую погоду&#9728; в вашем городе;\n"
                             "5. Перевод на {язык} {текст} - переведет текст на нужный язык&#128069;\n"
                             "6. Тест - пройдите тест, состоящий из 5 вопросов, и узнайте, как вы знаете щкольную программу&#128218;",
                     keyboard=create_keyboard(['Функции', 'Погода', 'Тест']).get_keyboard(),
                     random_id=random.randint(0, 2 ** 64))

def create_keyboard(options):
    # создание клавиатуры
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
    # из адреса получаем координаты
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

from datetime import datetime
import random

import requests
from vk_api.bot_longpoll import VkBotEventType

from data.users import User
from templates import geocoder, YES, NO, create_keyboard, FUNC, function


def add_city(user, db_sess, city):
    # обновление города в бд
    user.city = city
    db_sess.commit()


def get_text(city, response):
    # создание готового текста для сообщения
    return f"&#128204;Погода в городе {city}&#127751;\n" \
           f"{' в '.join(datetime.fromtimestamp(response['dt']).strftime('%d.%m.%Y %H:%M').split())}&#128337;\n" \
           f"Температура {response['main']['temp']}°C&#127777;\n" \
           f"Ощущается как {response['main']['feels_like']}°C&#10052;\n" \
           f"{response['weather'][0]['description'].capitalize()}. Ветер {response['wind']['speed']} м/с&#127788;"


def weather(id, db_sess, longpoll, vk):
    # взятие города для погоды
    user = db_sess.query(User).filter(User.id == id).first()
    if user.city:
        vk.messages.send(user_id=id,
                         message=f"Ваш город {user.city}?",
                         keyboard=create_keyboard(['Да', 'Нет', 'Стоп', 'Функции']).get_keyboard(),
                         random_id=random.randint(0, 2 ** 64))
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.obj.message['text'].lower() in NO:
                    vk.messages.send(user_id=id,
                                     message=f"Назовите, пожалуйста, свой город",
                                     keyboard=create_keyboard(['Стоп', 'Функции']).get_keyboard(),
                                     random_id=random.randint(0, 2 ** 64))
                    for event2 in longpoll.listen():
                        if event2.type == VkBotEventType.MESSAGE_NEW:
                            if event2.obj.message['text'].lower() in FUNC:
                                function(id, vk)
                            if event2.obj.message['text'].lower() in FUNC + ['стоп']:
                                break
                            city = event2.obj.message['text']
                            add_city(user, db_sess, city)
                            break
                    break
                elif event.obj.message['text'].lower() in YES:
                    city = user.city
                    break
                else:
                    vk.messages.send(user_id=id,
                                     message="Простите, я Вас не понял. Попробуйте ещё раз",
                                     random_id=random.randint(0, 2 ** 64))
                    vk.messages.send(user_id=id,
                                     message=f"Ваш город {user.city}?",
                                     random_id=random.randint(0, 2 ** 64))

    coords_data = geocoder(city)

    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'lat': coords_data[1],
        'lon': coords_data[0],
        'appid': '63784a82e085a2c186c0061c74e1d30e',
        'units': 'metric',
        'lang': 'ru'}
    response = requests.get(url=url, params=params)
    if not response:
        return None
    vk.messages.send(user_id=id,
                     message=get_text(city, response.json()),
                     keyboard=create_keyboard(['Функции']).get_keyboard(),
                     random_id=random.randint(0, 2 ** 64))

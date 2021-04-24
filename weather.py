from datetime import datetime
import random

import requests
from vk_api.bot_longpoll import VkBotEventType

from data.users import User
from templates import geocoder


def add_city(user, db_sess, city):
    user.city = city
    db_sess.commit()


def get_text(city, response):
    return f"Погода в городе {city}\n" \
           f"{' в '.join(datetime.fromtimestamp(response['dt'] + response['timezone']).strftime('%d.%m.%Y %H:%M').split())}.\n" \
           f"Температура {response['main']['temp']} °C.\n" \
           f"Ощущается как {response['main']['feels_like']}.\n" \
           f"{response['weather'][0]['description'].capitalize()}. Ветер {response['wind']['speed']} м/с."


def weather(id, db_sess, longpoll, vk):
    user = db_sess.query(User).filter(User.id == id).first()
    if user.city:
        vk.messages.send(user_id=id,
                         message=f"Ваш город {user.city}?",
                         random_id=random.randint(0, 2 ** 64))
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.obj.message['text'].lower() in ['нет']:
                    vk.messages.send(user_id=id,
                                     message=f"Назовите, пожалуйста, свой город",
                                     random_id=random.randint(0, 2 ** 64))
                    for event2 in longpoll.listen():
                        if event2.type == VkBotEventType.MESSAGE_NEW:
                            city = event2.obj.message['text']
                            add_city(user, db_sess, city)
                            break
                    break
                if event.obj.message['text'].lower() in ['да']:
                    city = user.city
                    break

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
                     random_id=random.randint(0, 2 ** 64))
import random
from datetime import datetime

import requests
from vk_api.bot_longpoll import VkBotEventType

from data.users import User
from module.maps import geocoder
from templates import YES, NO, FUNC


def get_text(city, response):
    return f"&#128204;Погода в городе {city}&#127751;\n" \
           f"{' в '.join(datetime.fromtimestamp(response['dt']).strftime('%d.%m.%Y %H:%M').split())}&#128337;\n" \
           f"Температура {response['main']['temp']}°C&#127777;\n" \
           f"Ощущается как {response['main']['feels_like']}°C&#10052;\n" \
           f"{response['weather'][0]['description'].capitalize()}. Ветер {response['wind']['speed']} м/с&#127788;"


def weather(city):
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
    return get_text(city, response.json())

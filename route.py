import random
from io import BytesIO

import requests
import vk_api

from templates import geocoder, create_keyboard


def route(id, address1, address2, vk):
    coords_data1  = geocoder(address1)
    coords_data2 = geocoder(address2)
    if not coords_data1 or not coords_data2:
        vk.messages.send(user_id=id,
                         message=f"Ой... Что-то пошло не так. Попробуйте ещё раз",
                         keyboard=create_keyboard(['Функции']).get_keyboard(),
                         random_id=random.randint(0, 2 ** 64))
        return None
    distance = ((float(coords_data1[0]) - float(coords_data2[0])) ** 2 +
                (float(coords_data1[1]) - float(coords_data2[1])) ** 2) ** 0.5 * 111
    coords1 = f'{coords_data1[0]},{coords_data1[1]}'
    coords2 = f'{coords_data2[0]},{coords_data2[1]}'
    map_params = {
        "l": 'map',
        'pt': f'{coords1},pm2al~{coords2},pm2bl'
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_api_server, params=map_params)
    if not response:
        vk.messages.send(user_id=id,
                         message=f"Ой... Что-то пошло не так. Попробуйте ещё раз",
                         keyboard=create_keyboard(['Функции']).get_keyboard(),
                         random_id=random.randint(0, 2 ** 64))
        return None
    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages(BytesIO(response.content))
    vk_photo_id = f"photo{photo[0]['owner_id']}_{photo[0]['id']}"
    vk.messages.send(peer_id=id,
                     message=f'Расстояние по прямой - {round(distance, 2)} км&#128663;',
                     keyboard=create_keyboard(['Функции']).get_keyboard(),
                     random_id=0, attachment=vk_photo_id)

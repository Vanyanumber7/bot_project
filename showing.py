import random
from io import BytesIO

import requests
import vk_api

from templates import geocoder


def showing(id, address, vk):
    coords_data = geocoder(address)
    if not coords_data:
        vk.messages.send(user_id=id,
                         message=f"Ой... Что-то пошло не так. Попробуйте ещё раз",
                         random_id=random.randint(0, 2 ** 64))
        return None
    coords = f'{coords_data[0]},{coords_data[1]}'
    delta = f'{abs(coords_data[2][0] - coords_data[3][0])},' \
            f'{abs(coords_data[2][1] - coords_data[3][1])}'

    map_params = {
        "ll": coords,
        "spn": delta,
        "l": 'map'
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_api_server, params=map_params)
    if not response:
        vk.messages.send(user_id=id,
                         message=f"Ой... Что-то пошло не так. Попробуйте ещё раз",
                         random_id=random.randint(0, 2 ** 64))
        return None
    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages(BytesIO(response.content))
    vk_photo_id = f"photo{photo[0]['owner_id']}_{photo[0]['id']}"
    vk.messages.send(peer_id=id, random_id=0, attachment=vk_photo_id)

    # pilimage = Image.open(BytesIO(response.content)).convert("RGBA")
    # map_file = pygame.image.fromstring(pilimage.tobytes(), pilimage.size, pilimage.mode)
    # return map_file, response.url, toponym_to_find[i]

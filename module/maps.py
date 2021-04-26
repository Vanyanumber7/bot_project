from io import BytesIO

import requests
import vk_api


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


def showing(coords_data, vk):
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
    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages(BytesIO(response.content))
    vk_photo_id = f"photo{photo[0]['owner_id']}_{photo[0]['id']}"
    return vk_photo_id


def route(coords_data1, coords_data2, vk):
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
    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages(BytesIO(response.content))
    vk_photo_id = f"photo{photo[0]['owner_id']}_{photo[0]['id']}"
    return vk_photo_id, distance

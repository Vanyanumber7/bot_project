from module.maps import *
from send.vk_send import *


def send_showing(vk, id, coords_data):
    if not coords_data:
        send(vk, id, f"Ой... Что-то пошло не так. Попробуйте ещё раз", keys=['Функции'])
        return None
    response = showing(coords_data, vk)
    if not response:
        send(vk, id, f"Ой... Что-то пошло не так. Попробуйте ещё раз", keys=['Функции'])
        return None
    send(vk, id, 'Карта', ['Функции'], response)


def send_route(vk, id, coords_data1, coords_data2):
    if not coords_data1 or not coords_data2:
        send(vk, id, f"Ой... Что-то пошло не так. Попробуйте ещё раз", keys=['Функции'])
        return None
    response, dist = route(coords_data1, coords_data2, vk)
    if not response or not dist:
        send(vk, id, f"Ой... Что-то пошло не так. Попробуйте ещё раз", keys=['Функции'])
        return None
    send(vk, id, f'Расстояние по прямой - {round(dist, 2)} км&#128663;', ['Функции'], response)

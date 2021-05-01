from send.vk_send import *


def send_wiki(vk, id, wiki_data):
    if not wiki_data:
        send(vk, id, f"Ой... Что-то пошло не так. Попробуйте ещё раз", keys=2)
        return None
    text, url = wiki_data
    # отправка сообщения
    send(vk, id, f"&#10071;{text}\n&#9889;Подробнее: {url}", keys=2)
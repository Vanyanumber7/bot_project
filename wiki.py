import random

import wikipedia

from templates import create_keyboard


def get_wiki(text):
    try:
        wikipedia.set_lang("ru")
        ny = wikipedia.page(text)
    except TypeError:
        return False
    return ny.content.split('\n')[0], ny.url


def wiki(id, vk, text):
    # взятие информации из википедии
    wiki_data = get_wiki(text)
    if not wiki_data:
        vk.messages.send(user_id=id,
                         message=f"Ой... Что-то пошло не так. Попробуйте ещё раз",
                         keyboard=create_keyboard(['Функции']).get_keyboard(),
                         random_id=random.randint(0, 2 ** 64))
    text, url = wiki_data
    # отправка сообщения
    vk.messages.send(user_id=id,
                     message=f"&#10071;{text}\n&#9889;Подробнее: {url}",
                     keyboard=create_keyboard(['Функции']).get_keyboard(),
                     random_id=random.randint(0, 2 ** 64))

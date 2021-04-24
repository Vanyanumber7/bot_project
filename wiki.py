import random

import wikipedia


def get_wiki(text):
    try:
        wikipedia.set_lang("ru")
        ny = wikipedia.page(text)
    except TypeError:
        return False
    return ny.content.split('\n')[0], ny.url


def wiki(id, vk, text):
    wiki_data = get_wiki(text)
    if wiki_data:
        text, url = wiki_data
    vk.messages.send(user_id=id,
                     message=f"{text}\nПодробнее: {url}",
                     random_id=random.randint(0, 2 ** 64))

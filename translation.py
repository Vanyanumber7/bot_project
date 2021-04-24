import random

from googletrans import Translator, constants

from templates import create_keyboard


def trans(text):
    # перевод с любого языка на английский
    trans = Translator()
    return trans.translate(text).text


def translation(id, text, lang, vk):
    try:
        translator = Translator()
        # перевод языка на английский
        lang = trans(lang).lower()
        print(lang)
        dict_of_lang = {}
        # переворот словаря языков
        for k, v in constants.LANGUAGES.items():
            dict_of_lang[v] = k
        print(dict_of_lang[lang])
        translation = translator.translate(text, dest=dict_of_lang[lang])
        vk.messages.send(user_id=id,
                         message='&#128216;' + translation.text + '&#128216;',
                         keyboard=create_keyboard(['Функции']).get_keyboard(),
                         random_id=random.randint(0, 2 ** 64))
    except Exception:
        vk.messages.send(user_id=id,
                         message='Не удалось перевести. Попробуйте в другой раз',
                         keyboard=create_keyboard(['Функции']).get_keyboard(),
                         random_id=random.randint(0, 2 ** 64))

from googletrans import Translator, constants


def trans(text):
    # перевод с любого языка на английский
    trans = Translator()
    return trans.translate(text).text


def translation(text, lang):
    try:
        translator = Translator()
        # перевод языка на английский
        lang = trans(lang).lower()
        dict_of_lang = {}
        # переворот словаря языков
        for k, v in constants.LANGUAGES.items():
            dict_of_lang[v] = k
        translation = translator.translate(text, dest=dict_of_lang[lang])
        return translation.text
    except Exception:
        return None

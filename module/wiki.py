import wikipedia


def wiki(text):
    # взятие информации из википедии
    try:
        wikipedia.set_lang("ru")
        ny = wikipedia.page(text)
    except TypeError:
        return False
    wiki_data = (ny.content.split('\n')[0], ny.url)
    return wiki_data

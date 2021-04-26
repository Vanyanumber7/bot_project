from send.vk_send import send


def send_translation(vk, id, text):
    if text:
        send(vk, id, '&#128216;' + text + '&#128216;', keys=['Функции'])
    else:
        send(vk, id, 'Не удалось перевести. Попробуйте в другой раз', keys=['Функции'])
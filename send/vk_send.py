import random

from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def create_keyboard(options):
    # создание клавиатуры
    keyboard = VkKeyboard(one_time=True)
    colors = [VkKeyboardColor.NEGATIVE, VkKeyboardColor.SECONDARY]
    i = -1
    for i in range(len(options) - 1):
        keyboard.add_button(options[i], color=colors[i % 2])
        keyboard.add_line()
    i += 1
    keyboard.add_button(options[-1], color=colors[i % 2])
    return keyboard


def send(vk, id, mes, keys=None, vk_photo_id=None):
    if keys == 2:
        keyboard = create_keyboard(['Функции']).get_keyboard()
    elif keys:
        keyboard = create_keyboard(keys).get_keyboard()
    else:
        keyboard = None
    vk.messages.send(user_id=id,
                     message=mes,
                     keyboard=keyboard,
                     random_id=random.randint(0, 2 ** 64),
                     attachment=vk_photo_id)


def function(id, vk):
    # функция для показа возможностей
    send(vk, id, "Вот что я могу:&#128540;\n"
                 "1. Что такое {что-то} - найдёт&#128269; нужное Вам понятие и даст ссылку на него\n"
                 "2. Покажи {что-то на карте} - отправит изображение&#128203; карты с нужным объектом\n"
                 "3. Маршрут {пункт А} | {пункт Б} - &#128205;отметит на карте эти точки и посчитает"
                 " расстояние по прямой&#128205;\n"
                 "4. Погода - выведет текущую погоду&#9728; в вашем городе;\n"
                 "5. Перевод на {язык} {текст} - переведет текст на нужный язык&#128069;\n"
                 "6. Тест - пройдите тест, состоящий из 5 вопросов, и узнайте, как вы знаете щкольную программу&#128218;",
         ['Функции', 'Погода', 'Тест'])

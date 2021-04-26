import logging
import random

from vk_api.bot_longpoll import VkBotEventType

from module.data_of_questions import *
from send.vk_send import send


def send_test(id, longpoll, vk):
    # провождение теста
    count_of_questions = -1
    count_of_currect_questions = -1
    send(vk, id, "Поехали!")
    # создание вопросов
    questions = [random.choice(maths), random.choice(geography), random.choice(biology),
                 random.choice(history),
                 random.choice(english), random.choice(physics)]
    # перемешивание ответов
    for i in range(len(questions)):
        random.shuffle(questions[i][1])
    # подсчет количества вопросов
    count_of_questions = len(questions)
    count_of_currect_questions = 0
    now_question = questions[len(questions) - count_of_questions]
    count_of_questions -= 1
    # отправка 1-ого сообщения
    send(vk, id, f"Вопрос {len(questions) - count_of_questions}! {now_question[0]}", now_question[1])
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            logging.info('Новое сообщение')
            logging.warning(f"Для меня от: {event.obj.message['from_id']}")
            logging.warning(f"Текст: {event.obj.message['text']}")


            if count_of_questions:
                # анализ ответа
                if event.obj.message['text'] in now_question[1]:
                    if event.obj.message['text'] == now_question[2]:
                        # правильный ответ
                        text = f"Правильно!&#128516;"
                        count_of_currect_questions += 1
                    else:
                        # неправильный ответ
                        text = f"Неправильно.&#128542;"
                    send(vk, id, text)
                    # смена текущего вопроса
                    now_question = questions[len(questions) - count_of_questions]
                    count_of_questions -= 1
                    # отправка вопроса
                    send(vk, id, f"Вопрос {len(questions) - count_of_questions}! {now_question[0]}", now_question[1])
                elif event.obj.message['text'].lower() == 'стоп':
                    # прекращение теста
                    send(vk, id, 'Принято', ['Функции'])
                    return None
                else:
                    # нет такого варианта ответа
                    send(vk, id, f"Ой...Такого варианта ответа нет. Попробуйте ещё раз", now_question[1])

            elif count_of_questions == 0:
                # последний вопрос
                if event.obj.message['text'] in now_question[1]:
                    if event.obj.message['text'] == now_question[2]:
                        text = f"Правильно!&#128516;"
                        count_of_currect_questions += 1
                    else:
                        text = f"Неправильно.&#128542;"
                    send(vk, id, text)
                elif event.obj.message['text'].lower() == 'стоп':
                    # прекращение теста
                    send(vk, id, 'Принято', ['Функции'])
                    return None
                else:
                    # ответ не из варианта
                    send(vk, id, f"Ой...Такого варианта ответа нет. Попробуйте ещё раз", now_question[1])
                # результат
                send(vk, id,
                     f'Ваш результат {count_of_currect_questions}/{len(questions)}.'
                     f'&#127881;&#127882;&#127881; Если хотите сыграть ещё раз, напишите "Тест"',
                     ['Функции'])
                return None

        else:
            pass

import random

from vk_api.bot_longpoll import VkBotEventType

from data_of_questions import *
from templates import create_keyboard


def test(id, longpoll, vk):
    count_of_questions = -1
    count_of_currect_questions = -1
    vk.messages.send(user_id=id,
                     message="Поехали!",
                     random_id=random.randint(0, 2 ** 64))
    questions = [random.choice(maths), random.choice(geography), random.choice(biology),
                 random.choice(history),
                 random.choice(english), random.choice(physics)]
    for i in range(len(questions)):
        random.shuffle(questions[i][1])
    count_of_questions = len(questions)
    count_of_currect_questions = 0
    now_question = questions[len(questions) - count_of_questions]
    count_of_questions -= 1
    vk.messages.send(user_id=id,
                     message=f"Вопрос {len(questions) - count_of_questions}! {now_question[0]}",
                     keyboard=create_keyboard(now_question[1]).get_keyboard(), random_id=random.randint(0, 2 ** 64))
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event)
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])

            if count_of_questions:
                if event.obj.message['text'] in now_question[1]:
                    if event.obj.message['text'] == now_question[2]:
                        text = f"Правильно!&#128516;"
                        count_of_currect_questions += 1
                    else:
                        text = f"Неправильно.&#128542;"
                    vk.messages.send(user_id=id, message=text, random_id=random.randint(0, 2 ** 64))
                    now_question = questions[len(questions) - count_of_questions]
                    count_of_questions -= 1
                    vk.messages.send(user_id=id,
                                     message=f"Вопрос {len(questions) - count_of_questions}! {now_question[0]}",
                                     keyboard=create_keyboard(now_question[1]).get_keyboard(),
                                     random_id=random.randint(0, 2 ** 64))
                elif event.obj.message['text'].lower() == 'стоп':
                    vk.messages.send(user_id=id,
                                     message='Принято',
                                     keyboard=create_keyboard(['Функции']).get_keyboard(),
                                     random_id=random.randint(0, 2 ** 64))
                    return None
                else:
                    vk.messages.send(user_id=id,
                                     message=f"Ой...Такого варианта ответа нет. Попробуйте ещё раз",
                                     keyboard=create_keyboard(now_question[1]).get_keyboard(),
                                     random_id=random.randint(0, 2 ** 64))

            elif count_of_questions == 0:
                if event.obj.message['text'] in now_question[1]:
                    if event.obj.message['text'] == now_question[2]:
                        text = f"Правильно!&#128516;"
                        count_of_currect_questions += 1
                    else:
                        text = f"Неправильно.&#128542;"
                    vk.messages.send(user_id=id, message=text, random_id=random.randint(0, 2 ** 64))
                elif event.obj.message['text'].lower() == 'стоп':
                    vk.messages.send(user_id=id,
                                     message='Принято',
                                     keyboard=create_keyboard(['Функции']).get_keyboard(),
                                     random_id=random.randint(0, 2 ** 64))
                    return None
                else:
                    vk.messages.send(user_id=id,
                                     message=f"Ой...Такого варианта ответа нет. Попробуйте ещё раз",
                                     random_id=random.randint(0, 2 ** 64))
                vk.messages.send(user_id=id,
                                 message=f'Ваш результат {count_of_currect_questions}/{len(questions)}.&#127881;&#127882;&#127881; Если хотите сыграть ещё раз, напишите "Старт"',
                                 keyboard=create_keyboard(['']).get_keyboard(),
                                 random_id=random.randint(0, 2 ** 64))
                return None

        else:
            pass

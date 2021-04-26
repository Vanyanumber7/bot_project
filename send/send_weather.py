from vk_api.bot_longpoll import VkBotEventType

from data.users import User
from module.weather import weather
from send.vk_send import *
from templates import *


def add_city(user, db_sess, city):
    user.city = city
    db_sess.commit()


def send_weather(id, db_sess, longpoll, vk):
    user = db_sess.query(User).filter(User.id == id).first()
    if user.city:
        send(vk, id, f"Ваш город {user.city}?",
             keys=['Да', 'Нет', 'Стоп', 'Функции'])
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.obj.message['text'].lower() in NO:
                    send(vk, id, f"Назовите, пожалуйста, свой город",
                                     keys=['Стоп', 'Функции'])
                    for event2 in longpoll.listen():
                        if event2.type == VkBotEventType.MESSAGE_NEW:
                            if event2.obj.message['text'].lower() in FUNC:
                                function(id, vk)
                            if event2.obj.message['text'].lower() in FUNC + ['стоп']:
                                break
                            city = event2.obj.message['text']
                            add_city(user, db_sess, city)
                            break
                    break
                elif event.obj.message['text'].lower() in YES:
                    city = user.city
                    break
                else:
                    send(vk, id, "Простите, я Вас не понял. Попробуйте ещё раз")
                    send(vk, id, f"Ваш город {user.city}?")
    else:
        send(vk, id, f"Назовите, пожалуйста, свой город", ['Стоп', 'Функции'])
        vk.messages.send(user_id=id,
                         message=f"Назовите, пожалуйста, свой город",
                         keyboard=create_keyboard(['Стоп', 'Функции']).get_keyboard(),
                         random_id=random.randint(0, 2 ** 64))
        for event2 in longpoll.listen():
            if event2.type == VkBotEventType.MESSAGE_NEW:
                if event2.obj.message['text'].lower() in FUNC:
                    function(id, vk)
                if event2.obj.message['text'].lower() in FUNC + ['стоп']:
                    break
                city = event2.obj.message['text']
                add_city(user, db_sess, city)
                break
    send(vk, id, weather(city), ['Функции'])


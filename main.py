import random
from string import punctuation

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import flask

from data import db_session
from data.users import User
from logpass import *
from route import route
from showing import showing
from test import test
from translation import translation
from weather import weather
from wiki import wiki
from templates import *

def users(info, user, db_sess):
    user.id = info['id']
    user.last_name = info['last_name']
    user.first_name = info['first_name']
    user.can_access_closed = info['can_access_closed']
    user.is_closed = info['is_closed']
    try:
        user.bdate = info['bdate']
    except KeyError:
        pass
    try:
        if not user.city:
            user.city = info['city']['title']
    except KeyError:
        pass
    try:
        user.sex = info['sex']
    except KeyError:
        pass
    try:
        user.domain = info['domain']
    except KeyError:
        pass
    db_sess.commit()


def add_users(info, db_sess):
    user = User()
    db_sess.add(user)
    users(info, user, db_sess)


def update_users(info, user, db_sess):
    users(info, user, db_sess)


def main():
    vk_session = vk_api.VkApi(token=TOKEN)
    longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:

            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])

            vk = vk_session.get_api()
            info = vk.users.get(user_id=event.obj.message['from_id'], fields="bdate,city,domain,sex")[0]

            db_session.global_init("db/data_of_users.db")
            db_sess = db_session.create_session()
            now_user = db_sess.query(User).filter(User.id == info['id']).first()
            if not now_user:
                add_users(info, db_sess)
            else:
                update_users(info, now_user, db_sess)

            print(info)
            id = info['id']
            text = event.obj.message['text'].translate(punctuation).lower().split()
            text_lower = event.obj.message['text'].translate(punctuation).lower()
            if text[:2] in WHAT_IS_IT:
                wiki(id, vk, text[2:])
            elif text[0] in SHOW:
                showing(id, ' '.join(text[1:]), vk)
            elif text[0] in ROUTER:
                address1, address2 = ' '.join(text[1:]).split('|')
                route(id, address1, address2, vk)
            elif text[0] in WEATHER_WORDS:
                weather(id, db_sess, longpoll, vk)
            elif text[0] in TRANSLATE:
                translation(id, ' '.join(event.obj.message['text'].split()[3:]), text[2], vk)
            elif text_lower in HELLO_QUESTION:
                vk.messages.send(user_id=id,
                                 message=random.choice(HELLO_ANSWER),
                                 keyboard=create_keyboard(['Функции']).get_keyboard(),
                                 random_id=random.randint(0, 2 ** 64))
            elif text_lower in HOW_ARE_YOU:
                vk.messages.send(user_id=id,
                                 message=random.choice(I_AM_FINE),
                                 keyboard=create_keyboard(['Функции']).get_keyboard(),
                                 random_id=random.randint(0, 2 ** 64))
            elif text_lower in FUNC:
                function(id, vk)
            elif text[0] == 'тест':
                test(id, longpoll, vk)
            else:
                vk.messages.send(user_id=id,
                                 message='Простите, я Вас не понял. Попробуйте ещё раз',
                                 keyboard=create_keyboard(['Функции']).get_keyboard(),
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()

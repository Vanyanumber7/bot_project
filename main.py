from string import punctuation

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

from data import db_session
from data.users import User
from logpass import *
from wiki import wiki


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
            text = event.obj.message['text'].translate(punctuation).lower().split()
            if text[:2] in [['что', 'такое'], ['кто', 'такой']]:
                wiki(info['id'], vk, text[2:])
            elif text[0] in ['покажи']:
                pass

if __name__ == '__main__':
    main()

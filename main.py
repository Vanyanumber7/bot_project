import logging
from string import punctuation

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from data import db_session
from data.users import User
from logpass import *
from module.translation import translation
from module.wiki import wiki
from send.send_test import send_test
from send.send_wiki import send_wiki
from send.send_maps import *
from send.send_translation import send_translation
from send.send_weather import send_weather
from send.vk_send import *
from templates import *

logging.basicConfig(
    filename='example.log',
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)


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
            logging.info(event)
            logging.warning('Для меня от:', event.obj.message['from_id'])
            logging.warning('Текст:', event.obj.message['text'])

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
                send_wiki(vk, id, wiki(text[2:]))
            elif text[0] in SHOW:
                send_showing(vk, id, geocoder(text[1:]))
            elif text[0] in ROUTER:
                address1, address2 = ' '.join(text[1:]).split('|')
                send_route(vk, id, geocoder(address1), geocoder(address2))
            elif text[0] in WEATHER_WORDS:
                send_weather(id, db_sess, longpoll, vk)
            elif text[0] in TRANSLATE:
                send_translation(vk, id, translation(' '.join(event.obj.message['text'].split()[3:]), text[2]))
            elif text_lower in HELLO_QUESTION:
                send(vk, id, random.choice(HELLO_ANSWER), ['Функции'])
            elif text_lower in FUNC:
                function(id, vk)
            elif text[0] == 'тест':
                send_test(id, longpoll, vk)
            else:
                send(vk, id, 'Простите, я Вас не понял. Попробуйте ещё раз', ['Функции'])


if __name__ == '__main__':
    main()

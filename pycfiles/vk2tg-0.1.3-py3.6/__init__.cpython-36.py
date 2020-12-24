# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vk2tg/__init__.py
# Compiled at: 2018-06-09 09:00:20
# Size of source mod 2**32: 1523 bytes
import logging
from telebot import TeleBot
from vk_api import VkApi, longpoll as vk_longpoll
__version__ = '0.1.3'
log_format = '%(asctime)s [%(filename)s:%(lineno)d] [%(levelname)s] %(name)s: "%(message)s"'
logging.basicConfig(format=log_format, level=(logging.WARNING))
logger = logging.getLogger('Vk2Tg')

class Vk2Tg:

    def __init__(self, tg_token=None, vk_token=None):
        self.tg = TeleBot(tg_token)
        self.vk_session = VkApi(token=vk_token)
        self.vk = self.vk_session.get_api()
        self.longpoll = vk_longpoll.VkLongPoll(self.vk_session)
        self.event_listeners = []

    def set_event_listener(self, listener):
        self.event_listeners.append(listener)

    def vk_listen(self):
        return self.longpoll.listen()

    def vk_polling(self):
        logger.info('Started vk_polling')
        while True:
            for event in self.vk_listen():
                for listener in self.event_listeners:
                    listener(event)

    @staticmethod
    def event_to_dict(event):
        res = dict()
        for attr in vk_longpoll.EVENT_ATTRS_MAPPING[event.type]:
            res[attr] = event.__getattribute__(attr)

        return res

    def send_tg_message(self, chat_id, event=None):
        if event is not None:
            text = '[{}] {}'.format(event.type, self.event_to_dict(event))
            self.tg.send_message(chat_id, text)
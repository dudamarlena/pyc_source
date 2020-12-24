# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/catchbot/router_bot.py
# Compiled at: 2018-06-23 13:58:03
# Size of source mod 2**32: 654 bytes
import logging, os
from .updater import create_updater
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  level=(logging.INFO))

class RouterBot:

    def __init__(self, token):
        self.updater = create_updater(token)

    @classmethod
    def from_env(cls):
        bot_token = os.environ['CATCHBOT_TOKEN']
        return RouterBot(bot_token)

    def start(self):
        self.updater.start_polling()

    def send_message(self, chat_id, text, parse_mode=None):
        self.updater.bot.send_message(chat_id=chat_id,
          text=text,
          parse_mode=parse_mode)
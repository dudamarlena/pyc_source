# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
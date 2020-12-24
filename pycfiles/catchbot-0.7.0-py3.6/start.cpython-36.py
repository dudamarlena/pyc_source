# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/catchbot/commands/start.py
# Compiled at: 2018-06-23 13:58:03
# Size of source mod 2**32: 572 bytes
import os

def _hook_url(chat_id):
    return '{protocol}://{host}/hooks/{chat_id}/{hash}'.format(protocol='http',
      host=(os.environ['CATCHBOT_GLOBAL_HOST']),
      chat_id=chat_id,
      hash='kljgfvgerf')


def start(bot, update):
    bot.send_message(chat_id=(update.message.chat_id),
      text=('\n'.join([
     'Hi!',
     '',
     "I'm the bot to catch your hooks",
     '',
     'Send your hooks here: {}'.format(_hook_url(update.message.chat_id))])))
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/catchbot/tasks.py
# Compiled at: 2018-06-23 13:58:03
# Size of source mod 2**32: 244 bytes
from catchbot.router_bot import RouterBot
from .celery_app import app
try:
    bot = RouterBot.from_env()
except:
    print('Failed to create bot')

@app.task
def send_message_to_bot(chat_id, message):
    bot.send_message(chat_id, message)
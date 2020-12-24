# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
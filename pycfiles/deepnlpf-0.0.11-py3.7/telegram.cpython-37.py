# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deepnlpf/modules/notifications/telegram.py
# Compiled at: 2019-09-21 11:59:36
# Size of source mod 2**32: 694 bytes
"""
    Date: 02/11/2018
   
              https://core.telegram.org/bots
    Tutorial: https://www.marcodena.it/blog/telegram-logging-handler-for-python-java-bash/
"""
import requests
import deepnlpf.config.notification as setting

class Telegram(object):

    def __init__(self):
        pass

    def send_message(self, message):
        payload = {'chat_id':setting.TELEGRAM['CHAT_ID'], 
         'text':message, 
         'parse_mode':'HTML'}
        if setting.TELEGRAM['SEND_MSG']:
            return requests.post('https://api.telegram.org/bot{token}/sendMessage'.format(token=(setting.TELEGRAM['TOKEN'])), data=payload).content
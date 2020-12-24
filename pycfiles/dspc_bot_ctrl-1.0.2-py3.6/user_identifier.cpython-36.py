# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dspc_bot_ctrl\user_identifier.py
# Compiled at: 2020-03-16 09:57:24
# Size of source mod 2**32: 2653 bytes
from telegram.ext import *
import logging, time, telegram
from telegram.error import *
import requests, json
from dspc_bot_ctrl.telegram_poller import TelegramPoller
lformat = '[*] %(asctime)s ::: %(levelname)s - %(message)s'
logging.basicConfig(format=lformat)
logger = logging.getLogger('pccbot_log')
logger.setLevel(logging.DEBUG)

class UserIdentifier:
    IDENTIFICATION_STATUS = False
    identification_handle = 'identify_me'

    def __init__(self, tmp_ROOT, telegram_token, password):
        self.password = password
        self.telegram_token = telegram_token
        self.tmp_ROOT = tmp_ROOT

    def identify(self):
        updates_api_link = 'https://api.telegram.org/bot' + self.telegram_token + '/getUpdates'
        logger.info("Please send 'identify_me <inputed_password>' to the bot throught the client to help the bot recognize you (This is done for security purposes).")
        logger.info('Looking out for identification message...')
        while self.IDENTIFICATION_STATUS == False:
            time.sleep(2)
            try:
                updates_data = json.loads(requests.get(updates_api_link).content)['result']
            except:
                logger.critical('Error in initializing identification sequence. Check your internet connection or your bot token.')
                exit()

            if len(updates_data) == 0:
                pass
            else:
                for update in updates_data:
                    text = update['message']['text']
                    if text.split(' ')[0].lower() == self.identification_handle:
                        if self.password in text:
                            chat_id = update['message']['chat']['id']
                            fn = update['message']['from']['first_name']
                            logger.info("Recognized identification token from '{}'".format(fn))
                            recognization_message = 'Identification successful. Now you can control your PC securely.'
                            requests.get('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(self.telegram_token, chat_id, recognization_message))
                            help_message = 'Type commands to see all valid commands.'
                            requests.get('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(self.telegram_token, chat_id, help_message))
                            self.IDENTIFICATION_STATUS = True
                            TelegramPoller(self.tmp_ROOT, chat_id, self.telegram_token).start()
                            break

                if self.IDENTIFICATION_STATUS == True:
                    break
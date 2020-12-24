# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/tmp/test/lib/python2.7/site-packages/pyrowire/resources/settings.py
# Compiled at: 2014-11-25 17:55:11
import logging
TOPICS = {'my_topic': {'send_on_accept': False, 
                'accept_response': "Great, we'll get right back to you.", 
                'error_response': 'It seems like an error has occurred...please try again later.', 
                'validators': {'profanity': 'You kiss your mother with that mouth? No profanity, please.', 
                               'length': 'Your message exceeded the maximum allowable character limit (or was empty). Please try again .', 
                               'parseable': 'Please only use alphanumeric and punctuation characters.'}, 
                'properties': {}, 'twilio': {'account_sid': '', 
                           'auth_token': '', 
                           'from_number': '+1234567890'}, 
                'max_message_length': 160}}
PROFILES = {'dev': {'debug': True, 
           'log_level': logging.DEBUG, 
           'redis': {'host': 'localhost', 
                     'port': 6379, 
                     'db': 0, 
                     'password': ''}, 
           'host': 'localhost', 
           'port': 62023}, 
   'staging': {'debug': True, 
               'log_level': logging.WARN, 
               'redis': {'host': 'localhost', 
                         'port': 6379, 
                         'db': 0, 
                         'password': ''}, 
               'host': '0.0.0.0', 
               'port': 0}, 
   'prod': {'debug': False, 
            'log_level': logging.ERROR, 
            'redis': {'host': 'localhost', 
                      'port': 6379, 
                      'db': 0, 
                      'password': ''}, 
            'host': '0.0.0.0', 
            'port': 0}}
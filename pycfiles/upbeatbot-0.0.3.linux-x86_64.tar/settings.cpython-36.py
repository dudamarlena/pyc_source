# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ndibari/development/UpBeatBot/venv/lib/python3.6/site-packages/upbeatbot/settings.py
# Compiled at: 2020-03-08 17:39:03
# Size of source mod 2**32: 564 bytes
import os
from envparse import env
env.read_envfile('.env')
LOG_FILE = os.environ.get('LOG_FILE', 'dev.log')
DEBUG = env.bool('DEBUG', default=False)
SLEEP_TIMEOUT = env.int('SLEEP_TIMEOUT', default=300)
CONSUMER_KEY = env.str('CONSUMER_KEY', default='__consumer_key_not_set__')
CONSUMER_SECRET = env.str('CONSUMER_SECRET', default='__consumer_secret_not_set__')
ACCESS_TOKEN = env.str('ACCESS_TOKEN', default='__access_token_not_set__')
ACCESS_TOKEN_SECRET = env.str('ACCESS_TOKEN_SECRET', default='__access_token_secret_not_set__')
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/brian/workspace/envs/envs/test_settings.py
# Compiled at: 2017-05-01 15:38:01
# Size of source mod 2**32: 158 bytes
from envs import env
DATABASE_URL = env('DATABASE_URL')
DEBUG = env('DEBUG', False, var_type='boolean')
MIDDLEWARE = env('MIDDLEWARE', [], var_type='list')
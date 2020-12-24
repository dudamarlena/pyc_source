# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/brian/workspace/envs/envs/test_settings.py
# Compiled at: 2017-11-25 11:35:48
# Size of source mod 2**32: 159 bytes
from envs import env
DATABASE_URL = env('DATABASE_URL')
DEBUG = env('DEBUG', False, var_type='boolean')
MIDDLEWARE = env('MIDDLEWARE', [], var_type='list')
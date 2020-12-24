# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/paicli/cmd.py
# Compiled at: 2019-07-22 01:15:24
# Size of source mod 2**32: 436 bytes
import json, getpass
from .utils import to_str

def token(api, expiration):
    password = ''
    if api.config.password:
        password = api.config.password
    else:
        password = to_str(getpass.getpass('Enter password:\n'))
    ret = api.post_token(api.config.username, password, expiration)
    token = json.loads(ret)['token']
    api.config.access_token = token
    api.config.write_access_token()
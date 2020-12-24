# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/age/.virtualenvs/twine/lib/python3.6/site-packages/joom/utils.py
# Compiled at: 2017-12-13 07:39:22
# Size of source mod 2**32: 271 bytes
import json

def build_response(resp):
    b = json.loads(resp.text)
    if resp.status_code == 200:
        if b['code'] == 0:
            if 'data' in b:
                return b['data']
            return b
    raise ValueError(b['message'])
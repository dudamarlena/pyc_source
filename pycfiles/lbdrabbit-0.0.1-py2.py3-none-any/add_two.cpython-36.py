# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/lbdrabbit-project/lbdrabbit/example/handlers/rpc/add_two.py
# Compiled at: 2019-10-06 23:15:05
# Size of source mod 2**32: 186 bytes
import json

def handler(event, context):
    print(event)
    return {'status_code':'200', 
     'body':json.dumps(event['a'] + event['b'])}
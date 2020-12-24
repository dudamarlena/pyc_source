# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cleber/.pyenv/versions/powerlibs_aws_sqs/lib/python3.6/site-packages/powerlibs/aws/sqs/dequeuer/handler.py
# Compiled at: 2017-09-19 11:49:54
# Size of source mod 2**32: 298 bytes
import json
from .exceptions import MessageIgnored

def handle_message(queue_name, message, handler):
    body = json.loads(message.body)
    payload = json.loads(body['Message'])
    try:
        handler(queue_name, body, payload)
    except MessageIgnored:
        return
    else:
        message.delete()
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\operation\abandon.py
# Compiled at: 2020-02-23 02:01:39
"""
"""
from ..protocol.rfc4511 import AbandonRequest, MessageID

def abandon_operation(msg_id):
    request = AbandonRequest(MessageID(msg_id))
    return request


def abandon_request_to_dict(request):
    return {'messageId': str(request)}
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\client\entity\event_remove.py
# Compiled at: 2020-04-23 03:19:47
# Size of source mod 2**32: 1144 bytes
from bsn_sdk_py.common import myecdsa256
from bsn_sdk_py.client.config import Config
from bsn_sdk_py.client.entity.bsn_base import BsnBase
from bsn_sdk_py.until.tools import nonce_str, array_sort, map_sort

class EventRemove(BsnBase):
    __doc__ = '\n    链码事件注销\n    '

    def __init__(self, eventId):
        self.eventId = eventId

    def req_body(self):
        req_body = {'eventId': self.eventId}
        return req_body

    def sign(self, body):
        sign_str = self.config.user_code + self.config.app_code + body['body']['eventId']
        mac = self.config.encrypt_sign.sign(sign_str).decode()
        return mac

    def verify(self, res_data):
        verify_str = str(res_data['header']['code']) + res_data['header']['msg']
        signature = res_data['mac']
        return self.config.encrypt_sign.verify(verify_str, signature)
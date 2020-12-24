# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\client\entity\event_register.py
# Compiled at: 2020-04-23 03:19:47
# Size of source mod 2**32: 1593 bytes
from bsn_sdk_py.common import myecdsa256
from bsn_sdk_py.client.config import Config
from bsn_sdk_py.client.entity.bsn_base import BsnBase
from bsn_sdk_py.until.tools import nonce_str, array_sort, map_sort

class EventRegister(BsnBase):
    """EventRegister"""

    def __init__(self, chainCode, eventKey, notifyUrl, attachArgs=''):
        self.chainCode = chainCode
        self.eventKey = eventKey
        self.notifyUrl = notifyUrl
        self.attachArgs = attachArgs

    def req_body(self):
        req_body = {'chainCode':self.chainCode, 
         'eventKey':self.eventKey, 
         'notifyUrl':self.notifyUrl, 
         'attachArgs':self.attachArgs}
        return req_body

    def sign(self, body):
        sign_str = self.config.user_code + self.config.app_code + body['body']['chainCode'] + body['body']['eventKey'] + body['body']['notifyUrl'] + body['body']['attachArgs']
        mac = self.config.encrypt_sign.sign(sign_str).decode()
        return mac

    def verify(self, res_data):
        verify_str = str(res_data['header']['code']) + res_data['header']['msg'] + str(res_data['body']['eventId'])
        signature = res_data['mac']
        return self.config.encrypt_sign.verify(verify_str, signature)
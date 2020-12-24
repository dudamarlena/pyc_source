# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\client\entity\no_trust_trans.py
# Compiled at: 2020-04-23 03:19:48
# Size of source mod 2**32: 1778 bytes
from bsn_sdk_py.common import myecdsa256
from bsn_sdk_py.client.config import Config
from bsn_sdk_py.client.entity.bsn_base import BsnBase
from bsn_sdk_py.until.tools import nonce_str, array_sort, map_sort, obj_sort
from bsn_sdk_py.trans.not_trust_trans_request import NotTrustTransRequest

class NoTrustTrans(BsnBase):
    """NoTrustTrans"""

    def __init__(self, chainCode, funcName, userName, args=None, transientData=None):
        super().__init__()
        self.name = userName
        self.chainCode = chainCode
        self.funcName = funcName
        self.args = args
        self.transientData = transientData

    def req_body(self):
        transRequest = NotTrustTransRequest(self.chainCode, self.funcName, self.name, self.args, self.transientData)
        transRequest.set_config(self.config)
        transRequest_data = transRequest.notrust_trans_data()
        req_body = {'transData': transRequest_data}
        return req_body

    def sign(self, body):
        sign_str = self.config.user_code + self.config.app_code + body['body']['transData']
        mac = self.config.encrypt_sign.sign(sign_str).decode()
        return mac

    def verify(self, res_data):
        verify_str = str(res_data['header']['code']) + res_data['header']['msg'] + obj_sort(res_data['body']['blockInfo']) + obj_sort(res_data['body']['ccRes'])
        signature = res_data['mac']
        return self.config.encrypt_sign.verify(verify_str, signature)
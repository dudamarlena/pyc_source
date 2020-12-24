# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\client\entity\get_block_info.py
# Compiled at: 2020-04-23 03:19:47
# Size of source mod 2**32: 1692 bytes
from bsn_sdk_py.common import myecdsa256
from bsn_sdk_py.client.config import Config
from bsn_sdk_py.client.entity.bsn_base import BsnBase
from bsn_sdk_py.until.tools import nonce_str, array_sort, map_sort

class GetBlockInfo(BsnBase):
    __doc__ = '\n    获取块信息\n    '

    def __init__(self, blockNumber=0, blockHash='', txId=''):
        self.blockNumber = blockNumber
        self.blockHash = blockHash
        self.txId = txId

    def req_body(self):
        req_body = {'blockNumber':self.blockNumber, 
         'blockHash':self.blockHash, 
         'txId':self.txId}
        return req_body

    def sign(self, body):
        sign_str = self.config.user_code + self.config.app_code + str(body['body']['blockNumber']) + body['body']['blockHash'] + body['body']['txId']
        mac = self.config.encrypt_sign.sign(sign_str).decode()
        return mac

    def verify(self, res_data):
        verify_str = str(res_data['header']['code']) + res_data['header']['msg'] + str(res_data['body']['blockHash']) + str(res_data['body']['blockNumber']) + res_data['body']['preBlockHash'] + str(res_data['body']['blockSize']) + str(res_data['body']['blockTxCount']) + array_sort(res_data['body']['transactions'])
        signature = res_data['mac']
        return self.config.encrypt_sign.verify(verify_str, signature)
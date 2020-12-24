# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\client\config.py
# Compiled at: 2020-04-23 03:19:47
# Size of source mod 2**32: 2778 bytes
import json
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend
from bsn_sdk_py.common.api_requestor import APIRequestor
from bsn_sdk_py.client.bsn_enum import AppAlgorithmType
from bsn_sdk_py.common.bsn_encrypt import ECDSA, SM2
from bsn_sdk_py.client.exceptions import BsnException

class Config(object):
    __doc__ = '\n    定义一个通用的配置\n    '

    def __init__(self, user_code, app_code, nodeApi, mspDir, httpcert, app_public_cert_path, user_private_cert_path, debug=False):
        self.user_code = user_code
        self.app_code = app_code
        self.nodeApi = nodeApi
        self.mspDir = mspDir
        self.httpcert = httpcert
        self.user_private_cert_path = user_private_cert_path
        self.app_public_cert_path = app_public_cert_path
        self.app_info = None
        self.app_info = self.getAppInfo()
        self.setAlgorithm()

    def setAlgorithm(self):
        if self.app_info['algorithmType'] == AppAlgorithmType.AppAlgorithmType_R1.value:
            self.encrypt_sign = ECDSA(self.user_private_cert_path, self.app_public_cert_path)
        else:
            if self.app_info['algorithmType'] == AppAlgorithmType.AppAlgorithmType_SM2.value:
                self.encrypt_sign = SM2(self.user_private_cert_path, self.app_public_cert_path)
            else:
                raise BsnException('-1', '无效的证书类型')

    def getAppInfo(self):
        """
        统一获取应用信息：
        {'appName': 'sdk测试-密钥非托管', 'appType': 'fabric', 'caType': 2, 'algorithmType': 2,
        'mspId': 'OrgbNodeMSP', 'channelId': 'app0001202004161020152918451'}
        :return:
        """
        req_url = self.nodeApi + '/api/app/getAppInfo'
        req_data = self.build_body()
        res = APIRequestor().request_post(req_url, req_data)
        return res['body']

    def build_body(self):
        data = {'header':{'userCode':self.user_code, 
          'appCode':self.app_code}, 
         'body':None, 
         'mac':''}
        return data


def read_private(pri_key_file_path):
    pri_key_file = open(pri_key_file_path, 'rb')
    key_data = pri_key_file.read()
    pri_key_file.close()
    skey = load_pem_private_key(key_data, password=None, backend=(default_backend()))
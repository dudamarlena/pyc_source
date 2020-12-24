# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\common\api_requestor.py
# Compiled at: 2020-04-23 03:11:40
# Size of source mod 2**32: 1160 bytes
import requests
from bsn_sdk_py.client.exceptions import BsnException
from bsn_sdk_py.client.bsn_enum import ResCode
from bsn_sdk_py.until.bsn_logger import log_debug, log_info

class APIRequestor(object):

    def __init__(self, cert_path=False):
        self.cert_path = cert_path

    def request_post(self, req_url, data):
        log_info(('请求地址：', req_url))
        log_info(('请求数据：', data))
        headers = {'content-type': 'application/json'}
        res = requests.post(req_url, headers=headers, json=data, verify=(self.cert_path))
        resCode = res.status_code
        if resCode != 200:
            raise Exception('请求失败,http code为{}'.format(resCode))
        resBody = res.json()
        log_info(('接受到的响应：', resBody))
        if resBody['header']['code'] != ResCode.ResCode_Suc.value:
            raise BsnException(resBody['header']['code'], resBody['header']['msg'])
        return resBody

    def request_get(self):
        pass
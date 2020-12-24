# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.14/lib/python2.7/site-packages/qcloud_cos/cos_cred.py
# Compiled at: 2018-03-19 03:53:29
from cos_params_check import ParamCheck

class CredInfo(object):
    """CredInfo用户的身份信息"""

    def __init__(self, appid, secret_id, secret_key):
        self._appid = appid
        self._secret_id = secret_id
        self._secret_key = secret_key
        self._param_check = ParamCheck()

    def get_appid(self):
        return self._appid

    def get_secret_id(self):
        return self._secret_id

    def get_secret_key(self):
        return self._secret_key

    def check_params_valid(self):
        if not self._param_check.check_param_int('appid', self._appid):
            return False
        if not self._param_check.check_param_unicode('secret_id', self._secret_id):
            return False
        return self._param_check.check_param_unicode('secret_key', self._secret_key)

    def get_err_tips(self):
        u"""获取错误信息

        :return:
        """
        return self._param_check.get_err_tips()
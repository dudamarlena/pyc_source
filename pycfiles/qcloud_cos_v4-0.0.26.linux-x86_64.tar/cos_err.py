# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.14/lib/python2.7/site-packages/qcloud_cos/cos_err.py
# Compiled at: 2018-03-19 03:53:29


class CosErr(object):
    """sdk错误码"""
    PARAMS_ERROR = -1
    NETWORK_ERROR = -2
    SERVER_ERROR = -3
    UNKNOWN_ERROR = -4

    @staticmethod
    def get_err_msg(errcode, err_info):
        return {'code': errcode, 'message': err_info}
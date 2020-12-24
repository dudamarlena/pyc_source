# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: orloclient/exceptions.py
# Compiled at: 2017-03-30 12:48:51
from __future__ import print_function
__author__ = 'alforbes'

class OrloError(Exception):
    """ Root exception """
    pass


class ClientError(OrloError):
    """ Client error, e.g. http/400 """
    pass


class ServerError(OrloError):
    """ Server error, e.g. http/500 """
    pass


class ConnectionError(OrloError):
    """ Connection Error """
    pass


OrloClientError = ClientError
OrloServerError = ServerError
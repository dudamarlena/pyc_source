# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\AsyncSpider\exceptions.py
# Compiled at: 2018-03-10 13:44:21
# Size of source mod 2**32: 821 bytes
from concurrent.futures import TimeoutError
__all__ = ['BaseSpiderException',
 'FetcherException',
 'RequestFailError', 'DropRequest', 'TimeoutError',
 'SaverException',
 'ItemFailError', 'DropItem',
 'SpiderException',
 'ActionFailError']

class BaseSpiderException(Exception):
    pass


class FetcherException(BaseSpiderException):
    pass


class RequestFailError(FetcherException):
    pass


class DropRequest(RequestFailError):
    pass


class SaverException(BaseSpiderException):
    pass


class ItemFailError(SaverException):
    pass


class DropItem(ItemFailError):
    pass


class SpiderException(BaseSpiderException):
    pass


class ActionFailError(SpiderException):
    pass
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/exceptions.py
# Compiled at: 2020-02-03 23:11:43
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: PyCharm
@file: exceptions.py
@create at: 2017-12-13 14:14

这一行开始写关于本文件的说明与解释
"""

class CrwyException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class CrwyImportException(CrwyException):
    pass


class CrwyKafkaException(CrwyException):
    pass


class CrwyMnsException(CrwyException):
    pass


class CrwyDbException(CrwyException):
    pass


class CrwyExtendException(CrwyException):
    pass


class CrwyCookieValidException(CrwyException):
    pass


class CrwyScrapyPlugsException(CrwyException):
    pass
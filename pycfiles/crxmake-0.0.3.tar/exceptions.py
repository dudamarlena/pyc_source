# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/exceptions.py
# Compiled at: 2020-02-03 23:11:43
__doc__ = '\n@author: wuyue\n@contact: wuyue92tree@163.com\n@software: PyCharm\n@file: exceptions.py\n@create at: 2017-12-13 14:14\n\n这一行开始写关于本文件的说明与解释\n'

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
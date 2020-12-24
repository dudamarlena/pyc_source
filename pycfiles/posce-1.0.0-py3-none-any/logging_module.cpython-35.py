# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\procode\logging_module.py
# Compiled at: 2019-09-04 06:16:18
# Size of source mod 2**32: 279 bytes
from blltoapp_interface import BllToAppInterface

class Loggingm(object):

    def __init__(self):
        pass

    @classmethod
    def write_error(self, jsonparam):
        bll = BllToAppInterface('loggerm', 'write_error')
        bll.executefun(jsonparam)
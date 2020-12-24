# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
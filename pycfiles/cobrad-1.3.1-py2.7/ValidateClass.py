# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/app/CommonClass/ValidateClass.py
# Compiled at: 2016-07-15 00:10:26
from flask import session
from DataDictClass import DataDict
__author__ = 'lightless'
__email__ = 'root@lightless.me'

class ValidateClass(object):

    def __init__(self, req, *args):
        self.req = req
        self.args = args
        self.vars = DataDict()

    @staticmethod
    def check_login():
        if session.get('is_login') and session.get('is_login') == True:
            return True
        else:
            return False

    def check_args(self):
        for arg in self.args:
            _arg = self.req.form.get(arg)
            if not _arg or _arg == '':
                return (False, arg + ' can not be empty.')
            self.vars[arg] = _arg

        return (True, None)
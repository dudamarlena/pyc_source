# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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

        return (
         True, None)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/daniel_lamotte/sandbox/krankshaft/krankshaft/exceptions.py
# Compiled at: 2013-12-03 10:58:22


class KrankshaftError(Exception):
    pass


class KrankshaftErrorList(KrankshaftError):

    def __init__(self, errors):
        self.errors = errors

    def __str__(self):
        from pprint import pformat
        msg = pformat(self.errors)
        if '\n' in msg:
            msg = '\n' + msg
        return msg


class Abort(KrankshaftError):

    def __init__(self, response):
        self.response = response


class ExpectedIssue(KrankshaftError):
    pass


class InvalidOptions(KrankshaftError):
    pass


class QueryIssues(KrankshaftErrorList):
    pass


class ResolveError(KrankshaftError):
    pass


class ValueIssue(KrankshaftErrorList):
    pass
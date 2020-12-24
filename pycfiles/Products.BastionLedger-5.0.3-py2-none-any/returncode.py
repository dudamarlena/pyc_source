# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/returncode.py
# Compiled at: 2015-07-18 19:38:10
DEBUG = -500
INFO = -300
WARN = -100
OK = 0
FAIL = 100
ERROR = 400
FATAL = 900

class returncode:
    """
    Encapsulate a return code from a financial institution

    It needs this Zope shite to be accessible from Python Scripts ...
    """
    _codes = {DEBUG: 'Debug', INFO: 'Info', 
       WARN: 'Warning', 
       FAIL: 'Failure', 
       OK: 'Ok', 
       ERROR: 'Error', 
       FATAL: 'Fatal'}

    def __init__(self, ref, amount, rc, sev, msg, response):
        assert self._codes.has_key(sev), 'Unknown Severity: %s' % str(sev)
        self.reference = ref
        self.amount = amount
        self.returncode = rc
        self.severity = int(sev)
        self.message = msg
        self.response = response

    def prettySeverity(self):
        """
        return the string-version of the severity code
        """
        return self._codes[self.severity]

    def __str__(self):
        return '<returncode %s>' % self.__dict__.items()
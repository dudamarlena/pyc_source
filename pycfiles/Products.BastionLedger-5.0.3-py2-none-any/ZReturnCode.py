# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/ZReturnCode.py
# Compiled at: 2015-07-18 19:38:10
import AccessControl, operator, string
from AccessControl import ClassSecurityInfo
from Products.PythonScripts.standard import html_quote
from PortalContent import PortalContent
from returncode import returncode, DEBUG, INFO, WARN, OK, FAIL, ERROR, FATAL

class ZReturnCode(PortalContent, returncode):
    """
    Encapsulate a return code from a financial institution, making it persistable
    in a ZODB

    It needs this Zope shite to be accessible from Python Scripts ...
    """
    _security = ClassSecurityInfo()
    _security.declareObjectPublic()
    meta_type = 'ZReturnCode'
    _codes = {DEBUG: 'Debug', INFO: 'Info', 
       WARN: 'Warning', 
       OK: 'Ok', 
       ERROR: 'Error', 
       FATAL: 'Fatal'}
    _properties = ({'id': 'returncode', 'type': 'string', 'mode': 'r'}, {'id': 'severity', 'type': 'int', 'mode': 'r'}, {'id': 'reference', 'type': 'string', 'mode': 'r'}, {'id': 'amount', 'type': 'string', 'mode': 'r'}, {'id': 'message', 'type': 'string', 'mode': 'r'}, {'id': 'response', 'type': 'text', 'mode': 'r'})

    def __init__(self, id, ref, amount, rc, sev, msg, response=''):
        self.id = id
        returncode.__init__(self, ref, amount, rc, sev, msg, response)

    def prettySeverity(self):
        return self._codes[self.severity]

    def prettyResponse(self):
        return newline_to_br(self.response)

    def __str__(self):
        return '<table>%s</table>' % reduce(operator.add, map(lambda (x, y): '<tr><th align="left">%s</th><td>%s</td></tr>' % (
         x, html_quote(y)), self.__dict__.items()))


AccessControl.class_init.InitializeClass(ZReturnCode)
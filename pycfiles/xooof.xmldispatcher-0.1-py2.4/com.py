# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/xmldispatcher/clients/adapters/com.py
# Compiled at: 2008-10-01 10:39:43
import re, pythoncom
from xooof.xmldispatcher.interfaces.interfaces import *

def _fix(s):
    return s.replace('\r\n', '\n').decode('iso-8859-1')


class COMAdapter(IXMLDispatcher):
    """Abstract base class for adapters to the IXMLDispatcher COM interface"""
    __module__ = __name__

    def __init__(self):
        self.__xd = None
        return

    def _connect(self):
        """Return the COM IXMLDispatcher object"""
        raise RuntimeError, '_connect must be implemented by subclasses'

    _code_descr_re = re.compile('(\\S*)::(.*)', re.DOTALL | re.MULTILINE)

    def _splitCodeDescr(self, description):
        mo = self._code_descr_re.match(description)
        if mo is not None:
            return mo.groups()
        else:
            return (
             None, description)
        return

    def _handleError(self, errorData):
        self.__xd = None
        (hr, msg, exc, arg) = errorData
        if exc is None:
            raise XMLDispatcherSystemException(msg, '', hr)
        else:
            (wcode, source, text, helpFile, helpId, scode) = exc
            if scode == -2147217183:
                (code, descr) = self._splitCodeDescr(text)
                raise XMLDispatcherUserException(_fix(descr), _fix(source), code)
            elif scode == -2147220270:
                (code, descr) = self._splitCodeDescr(text)
                raise XMLDispatcherAppException(_fix(descr), _fix(source), code)
            else:
                raise XMLDispatcherSystemException(_fix(text), _fix(source), hex(scode))
        return

    def dispatchClassMethodXML(self, className, methodName, xmlRqst, sessionData):
        if self.__xd is None:
            self.__xd = self._connect()
        try:
            r = self.__xd.DispatchClassMethodXML(className, methodName, xmlRqst, sessionData)
            return r
        except pythoncom.com_error, errorData:
            self._handleError(errorData)

        return

    def dispatchNewInstanceMethodXML(self, className, methodName, xmlRqst, sessionData):
        if self.__xd is None:
            self.__xd = self._connect()
        try:
            r = self.__xd.DispatchNewInstanceMethodXML(className, methodName, xmlRqst, sessionData)
            return r
        except pythoncom.com_error, errorData:
            self._handleError(errorData)

        return

    def dispatchInstanceMethodXML(self, className, methodName, instanceId, xmlRqst, sessionData):
        if self.__xd is None:
            self.__xd = self._connect()
        try:
            r = self.__xd.DispatchInstanceMethodXML(className, methodName, instanceId, xmlRqst, sessionData)
            return r
        except pythoncom.com_error, errorData:
            self._handleError(errorData)

        return
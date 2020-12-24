# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/xmldispatcher/clients/adapters/javaxdclient.py
# Compiled at: 2008-10-01 10:39:43
import re
from xooof.xmldispatcher.interfaces.interfaces import *
import org.xooof.xmldispatcher.interfaces.XMLDispatcherException, org.xooof.xmldispatcher.interfaces.XMLDispatcherUserException, org.xooof.xmldispatcher.interfaces.XMLDispatcherAppException, org.xooof.xmldispatcher.interfaces.XMLDispatcherSystemException

class JavaXMLDispatcherClientAdapter(IXMLDispatcher):
    """ A jython adapter for any java XMLDispatcherClient implementation """
    __module__ = __name__

    def __init__(self, jxd):
        """ constructor from a Java XMLDispatcherClient instance """
        self.__jxd = jxd

    def _handleError(self, e):
        descr = e.getMessage()
        source = 'N/A'
        code = e.getCode()
        if isinstance(e, org.xooof.xmldispatcher.interfaces.XMLDispatcherUserException):
            raise XMLDispatcherUserException(descr, source, code)
        elif isinstance(e, org.xooof.xmldispatcher.interfaces.XMLDispatcherAppException):
            raise XMLDispatcherAppException(descr, source, code)
        elif isinstance(e, org.xooof.xmldispatcher.interfaces.XMLDispatcherSystemException):
            raise XMLDispatcherSystemException(descr, source, code)
        else:
            raise RuntimeError('unknown exception from java: ' + str(e))

    def dispatchClassMethodXML(self, className, methodName, xmlRqst, sessionData):
        self.__jxd.setSessionData(sessionData)
        try:
            xml = self.__jxd.dispatchClassMethodXML(className, methodName, xmlRqst)
            return (xml, self.__jxd.getSessionData())
        except org.xooof.xmldispatcher.interfaces.XMLDispatcherException, e:
            self._handleError(e)

    def dispatchNewInstanceMethodXML(self, className, methodName, xmlRqst, sessionData):
        self.__jxd.setSessionData(sessionData)
        try:
            xml = self.__jxd.dispatchNewInstanceMethodXML(className, methodName, xmlRqst)
            return (xml, self.__jxd.getSessionData())
        except org.xooof.xmldispatcher.interfaces.XMLDispatcherException, e:
            self._handleError(e)

    def dispatchInstanceMethodXML(self, className, methodName, instanceId, xmlRqst, sessionData):
        self.__jxd.setSessionData(sessionData)
        try:
            xml = self.__jxd.dispatchInstanceMethodXML(className, methodName, instanceId, xmlRqst)
            return (xml, self.__jxd.getSessionData())
        except org.xooof.xmldispatcher.interfaces.XMLDispatcherException, e:
            self._handleError(e)
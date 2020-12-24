# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/xmldispatcher/clients/adapters/httpform.py
# Compiled at: 2008-10-01 10:39:43
import re, urllib, urllib2
from types import UnicodeType
import xml.sax
from xml.sax import ContentHandler
from xooof.xmldispatcher.interfaces.interfaces import *
from xooof.xmldispatcher.tools.envelope.constants import *
from xooof.xmldispatcher.tools.marshallers import ErrorMarshaller

class HTTPFORMAdapter(IXMLDispatcher):
    __module__ = __name__

    def __init__(self, appName, url, urlopener=None):
        self.__appName = appName
        self.__url = url
        if urlopener is None:
            self.__urlopener = urllib2.build_opener()
        else:
            self.__urlopener = urlopener
        return

    def _dispatch(self, verb, className, methodName, instanceId, xmlRqst, sessionData):
        if type(xmlRqst) is UnicodeType:
            xmlRqst = xmlRqst.encode('utf-8')
        query = {XD_F_APPNAME: self.__appName, XD_F_VERB: verb, XD_F_CLASSNAME: className, XD_F_METHODNAME: methodName}
        if instanceId:
            query[XD_F_INSTANCEID] = instanceId
        if xmlRqst:
            query[XD_F_XMLRQST] = xmlRqst
        if sessionData:
            query[XD_F_SESSIONDATA] = sessionData
        try:
            f = self.__urlopener.open(self.__url, urllib.urlencode(query))
        except urllib2.HTTPError, e:
            if e.code != 510:
                raise
            else:
                errorString = e.read()
                e.close()
                ErrorMarshaller.unmarshallExceptionFromXML(errorString)
        else:
            try:
                try:
                    sessionData = f.info()['XMLDispatcher-SessionData']
                except KeyError:
                    sessionData = ''

                return (
                 f.read(), sessionData)
            finally:
                f.close()

    def dispatchClassMethodXML(self, className, methodName, xmlRqst, sessionData):
        return self._dispatch(XD_VERB_CLASS_METHOD, className, methodName, None, xmlRqst, sessionData)

    def dispatchNewInstanceMethodXML(self, className, methodName, xmlRqst, sessionData):
        return self._dispatch(XD_VERB_NEW_INSTANCE_METHOD, className, methodName, None, xmlRqst, sessionData)

    def dispatchInstanceMethodXML(self, className, methodName, instanceId, xmlRqst, sessionData):
        return self._dispatch(XD_VERB_INSTANCE_METHOD, className, methodName, instanceId, xmlRqst, sessionData)
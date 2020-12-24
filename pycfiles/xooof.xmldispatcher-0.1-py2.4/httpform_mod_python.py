# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/xmldispatcher/servers/adapters/httpform_mod_python.py
# Compiled at: 2008-10-01 10:39:54
import sys
from mod_python import apache, util
from xooof.xmldispatcher.interfaces.interfaces import *
from xooof.xmldispatcher.servers.interfaces import *
from xooof.xmldispatcher.tools.envelope.constants import *
from xooof.xmldispatcher.tools.marshallers import ErrorMarshaller
from xooof.xmldispatcher.servers.basic import xdserver

class ModPythonHttpFormXDRequest(xdserver.Request):
    __module__ = __name__


class ModPythonHttpFormHandler:
    """ A mod_python handler for XMLDispatcher requests using
    the httpform protocol """
    __module__ = __name__

    def __init__(self, handlersHead, requestClass=ModPythonHttpFormXDRequest, errorsWithNs=0):
        self.__handlersHead = handlersHead
        self.__requestClass = requestClass
        self.__errorsWithNs = errorsWithNs

    def handler(self, req):
        try:
            fs = util.FieldStorage(req, keep_blank_values=1)
            try:
                appName = fs[XD_F_APPNAME]
            except KeyError:
                appName = None

            verb = fs[XD_F_VERB]
            className = fs[XD_F_CLASSNAME]
            methodName = fs[XD_F_METHODNAME]
            try:
                instanceId = fs[XD_F_INSTANCEID]
            except KeyError:
                instanceId = None

            try:
                xmlRqst = fs[XD_F_XMLRQST]
            except KeyError:
                xmlRqst = ''

            try:
                sessionData = fs[XD_F_SESSIONDATA]
            except KeyError:
                sessionData = ''

            request = self.__requestClass()
            request.verb = verb
            request.appName = appName
            request.className = className
            request.methodName = methodName
            request.instanceId = instanceId
            request.xmlRqst = xmlRqst
            request.sessionData = sessionData.decode('base64')
            request.apache_req = req
            self.__handlersHead.process(request)
        except:
            req.status = 510
            req.content_type = 'text/xml; charset=utf-8'
            req.headers_out['Expires'] = '0'
            req.headers_out['Cache-Control'] = 'no-cache'
            req.send_http_header()
            req.write(ErrorMarshaller.marshallExceptionToXML(sys.exc_info(), 'utf-8', withNs=self.__errorsWithNs))
            return apache.OK
        else:
            if request.xmlRply.startswith('<'):
                req.content_type = 'text/xml; charset=utf-8'
            else:
                req.content_type = 'text/plain; charset=utf-8'
            req.headers_out['Expires'] = '0'
            req.headers_out['Cache-Control'] = 'no-cache'
            if request.sessionData:
                req.headers_out['XMLDispatcher-SessionData'] = request.sessionData.encode('base64').replace('\n', '')
            req.send_http_header()
            req.write(request.xmlRply)
            return apache.OK

        return
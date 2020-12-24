# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/xmldispatcher/servers/adapters/httpform_python.py
# Compiled at: 2008-10-01 10:39:54
import sys, BaseHTTPServer, urlparse, cgi
from xooof.xmldispatcher.interfaces.interfaces import *
from xooof.xmldispatcher.servers.interfaces import *
from xooof.xmldispatcher.tools.envelope.constants import *
from xooof.xmldispatcher.tools.marshallers import ErrorMarshaller
from xooof.xmldispatcher.servers.basic import xdserver

class PythonHttpFormXDRequest(xdserver.Request):
    __module__ = __name__


class PythonHttpFormHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """ A Subclass of BaseHTTPRequestHandler to handle XMLDispatcher
    requests using the httpform protocol """
    __module__ = __name__

    def __init__(self, errorsWithNs=0):
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self)
        self.__errorsWithNs = errorsWithNs

    def getHandlersHead(self, appName):
        raise RuntimeError('getHandlersHead must be overwritten')

    def makeRequest(self):
        return PythonHttpFormXDRequest()

    def dispatch(self, appName, verb, className, methodName, instanceId, xmlRqst, sessionData):
        request = self.makeRequest()
        request.verb = verb
        request.appName = appName
        request.className = className
        request.methodName = methodName
        request.instanceId = instanceId
        request.xmlRqst = xmlRqst
        request.sessionData = sessionData
        self.getHandlersHead(appName).process(request)
        return (request.xmlRply, request.sessionData)

    def do_GET(self):
        environ = {}
        environ['REQUEST_METHOD'] = 'GET'
        environ['CONTENT_TYPE'] = 'application/x-www-form-urlencoded'
        environ['QUERY_STRING'] = urlparse.urlsplit(self.path)[4]
        self._do_work(environ)

    def do_POST(self):
        environ = {}
        environ['REQUEST_METHOD'] = 'POST'
        if 'content-type' in self.headers:
            environ['CONTENT_TYPE'] = self.headers['content-type']
        if 'content-length' in self.headers:
            environ['CONTENT_LENGTH'] = self.headers['content-length']
        self._do_work(environ)

    def _do_work(self, environ):
        try:
            fs = cgi.FieldStorage(fp=self.rfile, environ=environ, keep_blank_values=1, strict_parsing=1)
            try:
                appName = fs[XD_F_APPNAME].value
            except KeyError:
                appName = None

            verb = fs[XD_F_VERB]
            className = fs[XD_F_CLASSNAME].value
            methodName = fs[XD_F_METHODNAME].value
            try:
                instanceId = fs[XD_F_INSTANCEID].value
            except KeyError:
                instanceId = None

            try:
                xmlRqst = fs[XD_F_XMLRQST].value
            except KeyError:
                xmlRqst = ''

            try:
                sessionData = fs[XD_F_SESSIONDATA].value
            except KeyError:
                sessionData = ''

            (xmlRply, sessionData) = self.dispatch(verb, appName, className, methodName, instanceId, xmlRqst, sessionData)
        except:
            self.send_response(510)
            self.send_header('Content-Type', 'text/xml; charset=utf-8')
            self.send_header('Expires', '0')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(ErrorMarshaller.marshallExceptionToXML(sys.exc_info(), 'utf-8', withNs=self.__errorsWithNs))
        else:
            self.send_response(200)
            if xmlRply.startswith('<'):
                self.send_header('Content-Type', 'text/xml; charset=utf-8')
            else:
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Expires', '0')
            self.send_header('Cache-Control', 'no-cache')
            if sessionData:
                self.send_header['XMLDispatcher-SessionData'] = sessionData
            self.end_headers()
            self.wfile.write(xmlRply)

        return


if __name__ == '__main__':
    from xooof.xmldispatcher.servers.basic.xdhandlers import NullHandler

    class MyHttpHandler(PythonHttpFormHandler):
        __module__ = __name__
        head = NullHandler()

        def getHandlersHead(self, appName):
            return self.head


    httpd = BaseHTTPServer.HTTPServer(('', 8000), MyHttpHandler)
    httpd.serve_forever()
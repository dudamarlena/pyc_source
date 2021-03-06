# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/paste/webkit/wktransaction.py
# Compiled at: 2006-10-22 17:01:02
"""
The Webware transaction object.  Responsible for creating the request
and response objects, and managing some parts of the request cycle.
"""
from wkrequest import HTTPRequest
from wkresponse import HTTPResponse
from wksession import Session
from wkapplication import Application

class Transaction(object):
    __module__ = __name__

    def __init__(self, environ, start_response):
        self._environ = environ
        self._start_response = start_response
        self._request = HTTPRequest(self, environ)
        self._response = HTTPResponse(self, environ, start_response)
        self._session = None
        self._application = None
        return

    def application(self):
        if self._application is None:
            self._application = Application(self)
        return self._application

    def request(self):
        return self._request

    def response(self):
        return self._response

    def setResponse(self, response):
        assert 0, 'The response cannot be set'

    def hasSession(self):
        if self._session is not None:
            return True
        return self.request().environ()['paste.session.factory'].has_session()

    def session(self):
        if not self._session:
            self._session = Session(self.request().environ()['paste.session.factory']())
        return self._session

    def setSession(self, session):
        self._session = session

    def servlet(self):
        return self._servlet

    def setServlet(self, servlet):
        self._servlet = servlet

    def duration(self):
        return self.response().endTime() - self.request().time()

    def errorOccurred(self):
        assert 0, 'Not tracked'

    def setErrorOccurred(self, flag):
        assert 0, 'Not tracked'

    def die(self):
        pass

    def writeExceptionReport(self, handler):
        assert 0, 'Not implemented'

    def runTransaction(self):
        __traceback_hide__ = True
        if self._session:
            self._session.awake(self)
        self._servlet.runTransaction(self)

    def forward(self, url):
        assert self._environ.has_key('paste.recursive.forward'), 'Forwarding is not supported (use the recursive middleware)'
        if url.startswith('/'):
            url = url[1:]
        app_iter = self._environ['paste.recursive.forward'](url)
        raise self._servlet.ReturnIterException(app_iter)
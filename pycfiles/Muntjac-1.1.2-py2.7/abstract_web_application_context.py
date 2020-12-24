# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/gwt/server/abstract_web_application_context.py
# Compiled at: 2013-04-04 15:36:36
"""Defines a base class for web application contexts that handles the common
tasks."""
import logging, urllib
from muntjac.service.application_context import IApplicationContext
from muntjac.terminal.gwt.server.web_browser import WebBrowser
logger = logging.getLogger(__name__)

class AbstractWebApplicationContext(IApplicationContext):
    """Base class for web application contexts that handles the common tasks.
    """

    def __init__(self):
        self.listeners = list()
        self.applications = set()
        self.browser = WebBrowser()
        self.applicationToAjaxAppMgrMap = dict()

    def addTransactionListener(self, listener):
        if listener is not None:
            self.listeners.append(listener)
        return

    def removeTransactionListener(self, listener):
        self.listeners.remove(listener)

    def startTransaction(self, application, request):
        """Sends a notification that a transaction is starting.

        @param application:
                   The application associated with the transaction.
        @param request:
                   the HTTP request that triggered the transaction.
        """
        for listener in self.listeners:
            listener.transactionStart(application, request)

    def endTransaction(self, application, request):
        """Sends a notification that a transaction has ended.

        @param application:
                   The application associated with the transaction.
        @param request:
                   the HTTP request that triggered the transaction.
        """
        exceptions = None
        for listener in self.listeners:
            try:
                listener.transactionEnd(application, request)
            except RuntimeError as t:
                if exceptions is None:
                    exceptions = list()
                exceptions.append(t)

        if exceptions is not None:
            msg = str()
            for e in exceptions:
                if len(msg) == 0:
                    msg += '\n\n--------------------------\n\n'
                msg += str(e) + '\n'

            raise RuntimeError(msg)
        return

    def valueBound(self, arg0):
        """@see: L{HttpSessionBindingListener.valueBound}"""
        pass

    def valueUnbound(self, event):
        """@see: L{HttpSessionBindingListener.valueUnbound}"""
        try:
            for app in self.applications:
                app.close()
                self.removeApplication(app)

        except Exception:
            logger.critical('Could not remove application, leaking memory.')

    def getBrowser(self):
        """Get the web browser associated with this application context.

        Because application context is related to the http session and server
        maintains one session per browser-instance, each context has exactly
        one web browser associated with it.
        """
        return self.browser

    def getApplications(self):
        return self.applications

    def removeApplication(self, application):
        self.applications.remove(application)
        if application in self.applicationToAjaxAppMgrMap:
            del self.applicationToAjaxAppMgrMap[application]

    def generateApplicationResourceURL(self, resource, mapKey):
        filename = resource.getFilename()
        if filename is None:
            return 'app://APP/' + mapKey + '/'
        else:
            encodedFileName = self.urlEncode(filename)
            return 'app://APP/' + mapKey + '/' + encodedFileName
            return

    def urlEncode(self, filename):
        return urllib.quote(filename, safe='/\\')

    def isApplicationResourceURL(self, context, relativeUri):
        if relativeUri is None:
            return False
        else:
            prefix = relativeUri
            index = relativeUri.find('/')
            if index >= 0:
                prefix = relativeUri[:index]
            return prefix == 'APP'

    def getURLKey(self, context, relativeUri):
        index = relativeUri.find('/')
        nxt = relativeUri.find('/', index + 1)
        if nxt < 0:
            return None
        else:
            return relativeUri[index + 1:nxt]
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/gwt/server/web_application_context.py
# Compiled at: 2013-04-04 15:36:36
"""Defines a web application context for Muntjac applications."""
from muntjac.terminal.gwt.server.abstract_web_application_context import AbstractWebApplicationContext
from muntjac.util import clsname

class WebApplicationContext(AbstractWebApplicationContext):
    """Web application context for Muntjac applications.

    This is automatically added as a L{HttpSessionBindingListener}
    when added to a L{HttpSession}.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def __init__(self):
        """Creates a new Web Application Context."""
        super(WebApplicationContext, self).__init__()
        self.session = None
        self._reinitializingSession = False
        self._currentRequest = None
        return

    def __getstate__(self):
        result = self.__dict__.copy()
        del result['session']
        del result['_reinitializingSession']
        del result['_currentRequest']
        return result

    def __setstate__(self, d):
        self.__dict__ = d
        self.session = None
        self._reinitializingSession = False
        self._currentRequest = None
        return

    def startTransaction(self, application, request):
        self._currentRequest = request
        super(WebApplicationContext, self).startTransaction(application, request)

    def endTransaction(self, application, request):
        super(WebApplicationContext, self).endTransaction(application, request)
        self._currentRequest = None
        return

    def valueUnbound(self, event):
        if not self._reinitializingSession:
            super(WebApplicationContext, self).valueUnbound(event)

    def reinitializeSession(self):
        """Discards the current session and creates a new session with
        the same contents. The purpose of this is to introduce a new
        session key in order to avoid session fixation attacks.
        """
        oldSession = self.getHttpSession()
        attrs = dict()
        attrs.update(oldSession.values)
        self._reinitializingSession = True
        oldSession.invalidate()
        self._reinitializingSession = False
        newSession = self._currentRequest.session()
        for name, val in attrs.iteritems():
            newSession.setValue(name, val)

        self.session = newSession

    def getBaseDirectory(self):
        """Gets the application context base directory.

        @see: L{ApplicationContext.getBaseDirectory}
        """
        realPath = self.getResourcePath(self.session, '/')
        if realPath is None:
            return
        else:
            return realPath

    def getHttpSession(self):
        """Gets the http-session application is running in.

        @return: HttpSession this application context resides in.
        """
        return self.session

    @classmethod
    def getApplicationContext(cls, session, servlet):
        """Gets the application context for an HttpSession.

        @param session:
                   the HTTP session.
        @return: the application context for HttpSession.
        """
        cx = servlet.getSessionAttribute(session, clsname(WebApplicationContext), None)
        if cx is None:
            cx = WebApplicationContext()
            servlet.setSessionAttribute(session, clsname(WebApplicationContext), cx)
        if cx.session is None:
            cx.session = session
        return cx

    def addApplication(self, application):
        self.applications.add(application)

    def getApplicationManager(self, application, servlet):
        """Gets communication manager for an application.

        If this application has not been running before, a new manager is
        created.

        @return: CommunicationManager
        """
        mgr = self.applicationToAjaxAppMgrMap.get(application)
        if mgr is None:
            mgr = servlet.createCommunicationManager(application)
            self.applicationToAjaxAppMgrMap[application] = mgr
        return mgr
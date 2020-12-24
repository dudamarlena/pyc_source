# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/gwt/server/gae_application_servlet.py
# Compiled at: 2013-04-04 15:36:36
from gaesessions import get_current_session
from muntjac.terminal.gwt.server.application_servlet import ApplicationServlet
from muntjac.terminal.gwt.server.abstract_application_servlet import RequestType
from muntjac.util import totalseconds

class GaeApplicationServlet(ApplicationServlet):
    SID = '0ce25c442d1f4fad8fb6eb44f24ff4a5e0df89e07ae97a3f'

    def service(self, request, response):
        requestType = self.getRequestType(request)
        if requestType == RequestType.UIDL:
            session = self.getSession(request, False)
            if session is not None and session.is_active():
                reqs = session.get('uidl_reqs', 0)
                session['uidl_reqs'] = reqs + 1
        super(GaeApplicationServlet, self).service(request, response)
        return

    def getSession(self, request, allowSessionCreation=True):
        if allowSessionCreation:
            return get_current_session()
        else:
            s = get_current_session()
            if s.is_active():
                return s
            return
            return

    def invalidateSession(self, request):
        session = self.getSession(request)
        session.terminate()

    def getSessionId(self, request):
        sid = get_current_session().sid
        return sid

    def getSessionAttribute(self, session, name, default=None):
        return session.get(name, default)

    def setSessionAttribute(self, session, name, value):
        session[name] = value

    def getMaxInactiveInterval(self, session):
        if session.lifetime is not None:
            return int(totalseconds(session.lifetime))
        else:
            return self._timeout
            return

    def isSessionNew(self, session):
        raise NotImplementedError
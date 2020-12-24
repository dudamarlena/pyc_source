# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/addon/invient/demo/invient_demo_app.py
# Compiled at: 2013-04-04 15:36:37
from muntjac.application import Application
from muntjac.addon.invient.demo.invient_demo_win import InvientChartsDemoWin
from muntjac.terminal.gwt.server.http_servlet_request_listener import IHttpServletRequestListener

class InvientChartsDemoApp(Application, IHttpServletRequestListener):

    def __init__(self):
        super(InvientChartsDemoApp, self).__init__()
        self._isAppRunningOnGAE = None
        return

    def isAppRunningOnGAE(self):
        if self._isAppRunningOnGAE is None:
            return False
        else:
            return self._isAppRunningOnGAE

    def init(self):
        self.setMainWindow(InvientChartsDemoWin())
        self.getMainWindow().showNotification('To hide a series, click on its legend label.')

    def onRequestStart(self, request, response):
        if self._isAppRunningOnGAE is None:
            self._isAppRunningOnGAE = False
        return

    def onRequestEnd(self, request, response):
        pass


if __name__ == '__main__':
    from muntjac.main import muntjac
    from invient_demo_app_servlet import InvientChartsDemoAppServlet
    muntjac(InvientChartsDemoApp, nogui=True, forever=True, debug=True, contextRoot='.')
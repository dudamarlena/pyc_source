# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/gwt/server/paste_deploy_application_servlet.py
# Compiled at: 2013-04-04 15:36:36
from paste.deploy import CONFIG
from muntjac.terminal.gwt.server.application_servlet import ApplicationServlet
from muntjac.terminal.gwt.server.exceptions import ServletException
from muntjac.util import loadClass

class app(ApplicationServlet):
    """Servlet for use with Paste Deploy."""
    SERVLET_PARAMETER_APPLICATION = 'application'

    def __init__(self):
        appClassName = CONFIG.get(self.SERVLET_PARAMETER_APPLICATION)
        if appClassName is None:
            raise ServletException, 'Application not specified in servlet parameters'
        try:
            applicationClass = loadClass(appClassName)
        except ImportError:
            raise ServletException, 'Failed to import module: ' + appClassName
        except AttributeError:
            raise ServletException, 'Failed to load application class: ' + appClassName

        super(app, self).__init__(applicationClass)
        self._applicationProperties.update(CONFIG)
        return
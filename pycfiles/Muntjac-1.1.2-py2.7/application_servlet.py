# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/gwt/server/application_servlet.py
# Compiled at: 2013-04-04 15:36:36
"""Defines a servlet that connects a Muntjac Application to Web."""
from muntjac.terminal.gwt.server.exceptions import ServletException
from muntjac.terminal.gwt.server.abstract_application_servlet import AbstractApplicationServlet

class ApplicationServlet(AbstractApplicationServlet):
    """This servlet connects a Muntjac Application to Web.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def __init__(self, applicationClass, *args, **kw_args):
        super(ApplicationServlet, self).__init__(*args, **kw_args)
        self._applicationClass = applicationClass

    def getNewApplication(self, request):
        try:
            applicationClass = self.getApplicationClass()
            application = applicationClass()
        except TypeError:
            raise ServletException, 'getNewApplication failed'

        return application

    def getApplicationClass(self):
        return self._applicationClass


class SingletonApplicationServlet(AbstractApplicationServlet):

    def __init__(self, applicationObject, *args, **kw_args):
        super(SingletonApplicationServlet, self).__init__(*args, **kw_args)
        self._applicationObject = applicationObject

    def getNewApplication(self, request):
        if self._applicationObject is not None:
            return self._applicationObject
        else:
            raise ServletException, 'getNewApplication failed'
            return

    def getApplicationClass(self):
        return self._applicationObject.__class__
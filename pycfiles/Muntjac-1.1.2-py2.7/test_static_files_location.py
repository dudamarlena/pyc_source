# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/terminal/gwt/server/test_static_files_location.py
# Compiled at: 2013-04-04 15:36:37
import mox
from urlparse import urlparse
from unittest import TestCase
from muntjac.terminal.gwt.server.application_servlet import ApplicationServlet
from paste.webkit.wkrequest import HTTPRequest

class TestStaticFilesLocation(TestCase):

    def setUp(self):
        super(TestStaticFilesLocation, self).setUp()
        self.mox = mox.Mox()
        self.servlet = ApplicationServlet(None)
        setattr(self.servlet, 'applicationProperties', {})
        return

    def testWidgetSetLocation(self):
        location = self._testLocation('http://dummy.host:8080', '/contextpath', '/servlet', '')
        self.assertEquals('/contextpath', location)
        location = self._testLocation('http://dummy.host:8080', '', '/servlet', '')
        self.assertEquals('', location)
        location = self._testLocation('http://dummy.host', '/contextpath', '/servlet', '/extra/stuff')
        self.assertEquals('/contextpath', location)
        location = self._testLocation('http://dummy.host', '/context/path', '/servlet', '/extra/stuff')
        self.assertEquals('/context/path', location)
        location = self._testIncludedLocation('http://my.portlet.server', '/user', '/tmpservletlocation1', '')
        self.assertEquals('Wrong widgetset location', '/user', location)

    def _testLocation(self, base, contextPath, servletPath, pathInfo):
        request = self.createNonIncludeRequest(base, contextPath, servletPath, pathInfo)
        mox.Replay(request)
        location = getattr(self.servlet, 'getStaticFilesLocation', request)
        return location

    def _testIncludedLocation(self, base, portletContextPath, servletPath, pathInfo):
        request = self.createIncludeRequest(base, portletContextPath, servletPath, pathInfo)
        mox.Replay(request)
        location = self._getStaticFilesLocationMethod(self.servlet, request)
        return location

    def createIncludeRequest(self, base, realContextPath, realServletPath, pathInfo):
        request = self.createRequest(base, '', '', pathInfo)
        request.getAttribute('javax.servlet.include.context_path').AndReturn(realContextPath).MultipleTimes()
        request.getAttribute('javax.servlet.include.servlet_path').AndReturn(realServletPath).MultipleTimes()
        request.getAttribute(ApplicationServlet.REQUEST_VAADIN_STATIC_FILE_PATH).AndReturn(None).MultipleTimes()
        return request

    def createNonIncludeRequest(self, base, realContextPath, realServletPath, pathInfo):
        request = self.createRequest(base, realContextPath, realServletPath, pathInfo)
        self.servlet.getParameter(request, 'javax.servlet.include.context_path', None).AndReturn(None).MultipleTimes()
        self.servlet.getParameter(request, 'javax.servlet.include.servlet_path', None).AndReturn(None).MultipleTimes()
        self.servlet.getParameter(request, ApplicationServlet.REQUEST_VAADIN_STATIC_FILE_PATH, None).AndReturn(None).MultipleTimes()
        return request

    def createRequest(self, base, contextPath, servletPath, pathInfo):
        """Creates a HttpServletRequest mock using the supplied parameters.

        @param base:
                   The base url, e.g. http://localhost:8080
        @param contextPath:
                   The context path where the application is deployed, e.g.
                   /mycontext
        @param servletPath:
                   The servlet path to the servlet we are testing, e.g. /myapp
        @param pathInfo:
                   Any text following the servlet path in the request, not
                   including query parameters, e.g. /UIDL/
        @return: A mock HttpServletRequest object useful for testing
        @raise MalformedURLException:
        """
        url = urlparse(base + contextPath + pathInfo)
        request = self.mox.CreateMock(HTTPRequest)
        self.servlet.isSecure(request).AndReturn(url.scheme().lower() == 'https').MultipleTimes()
        self.servlet.getServerName(request).AndReturn(url.hostname).MultipleTimes()
        self.servlet.getServerPort(request).AndReturn(url.port).MultipleTimes()
        self.servlet.getRequestURI(request).AndReturn(url.path).MultipleTimes()
        self.servlet.getContextPath(request).AndReturn(contextPath).MultipleTimes()
        self.servlet.getPathInfo(request).AndReturn(pathInfo).MultipleTimes()
        self.servlet.getServletPath(request).AndReturn(servletPath).MultipleTimes()
        return request
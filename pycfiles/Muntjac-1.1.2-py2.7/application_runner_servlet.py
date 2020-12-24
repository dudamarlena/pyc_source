# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/gwt/server/application_runner_servlet.py
# Compiled at: 2013-04-04 15:36:36
import re, logging
from muntjac.terminal.gwt.server.exceptions import ServletException
from muntjac.terminal.gwt.server.abstract_application_servlet import AbstractApplicationServlet
from muntjac.util import loadClass
logger = logging.getLogger(__name__)

class ApplicationRunnerServlet(AbstractApplicationServlet):

    def awake(self, transaction):
        super(ApplicationRunnerServlet, self).awake(transaction)
        self._defaultPackages = None
        self._request = None
        initParameter = self.getApplicationOrSystemProperty('defaultPackages', None)
        if initParameter is not None:
            self._defaultPackages = re.split(',', initParameter)
        return

    def respond(self, transaction):
        self._request = transaction.request()
        super(ApplicationRunnerServlet, self).respond(transaction)
        self._request = None
        return

    def getApplicationUrl(self, request):
        path = super(ApplicationRunnerServlet, self).getApplicationUrl(request)
        path += self.getApplicationRunnerApplicationClassName(request)
        path += '/'
        return path

    def getNewApplication(self, request):
        try:
            application = self.getApplicationClass()()
            return application
        except TypeError:
            raise ServletException('Failed to load application class: ' + self.getApplicationRunnerApplicationClassName(request))

    def getApplicationRunnerApplicationClassName(self, request):
        return self.getApplicationRunnerURIs(request).applicationClassname

    @classmethod
    def getApplicationRunnerURIs(cls, request):
        """Parses application runner URIs.

        If request URL is e.g.
        http://localhost:8080/muntjac/run/muntjac.demo.calc.Calc then

          - context=muntjac
          - Runner servlet=run
          - Muntjac application=muntjac.demo.calc.Calc

        @return: string array containing widgetset URI, application URI and
                context, runner, application classname
        """
        urlParts = re.split('\\/', request.uri())
        context = None
        uris = URIS()
        applicationClassname = None
        contextPath = cls.getContextPath(request)
        if urlParts[1] == re.sub('\\/', '', contextPath):
            context = urlParts[1]
            if len(urlParts) == 3:
                raise ValueError, 'No application specified'
            applicationClassname = urlParts[3]
            uris.staticFilesPath = '/' + context
            uris.applicationClassname = applicationClassname
        else:
            context = ''
            if len(urlParts) == 2:
                raise ValueError, 'No application specified'
            applicationClassname = urlParts[2]
            uris.staticFilesPath = '/'
            uris.applicationClassname = applicationClassname
        return uris

    def getApplicationClass(self):
        appClass = None
        baseName = self.getApplicationRunnerApplicationClassName(self._request)
        try:
            appClass = loadClass(baseName)
            return appClass
        except Exception:
            if self._defaultPackages is not None:
                for i in range(len(self._defaultPackages)):
                    try:
                        clsName = self._defaultPackages[i] + '.' + baseName
                        appClass = loadClass(clsName)
                    except TypeError:
                        pass
                    except Exception:
                        logger.info('Failed to find application class in the default package.')

                    if appClass is not None:
                        return appClass

        raise TypeError, 'class not found exception'
        return

    def getRequestPathInfo(self, request):
        path = self.getPathInfo(request)
        if path is None:
            return
        else:
            clsName = self.getApplicationRunnerApplicationClassName(request)
            path = path[1 + len(clsName):]
            return path

    def getStaticFilesLocation(self, request):
        uris = self._getApplicationRunnerURIs(request)
        staticFilesPath = uris.staticFilesPath
        if staticFilesPath == '/':
            staticFilesPath = ''
        return staticFilesPath


class URIS(object):

    def __init__(self):
        self.staticFilesPath = None
        self.applicationClassname = None
        return
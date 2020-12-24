# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/gwt/server/abstract_application_servlet.py
# Compiled at: 2013-04-04 15:36:36
"""Defines a servlet that handles all communication between the client and
the server."""
import re, logging, mimetypes
from time import time
from warnings import warn
from urlparse import urljoin
from os.path import exists, getmtime
try:
    from StringIO import StringIO
except ImportError as e:
    from StringIO import StringIO

from muntjac.util import clsname
from muntjac.application import Application
from muntjac.terminal.gwt.server.constants import Constants
from muntjac.terminal.gwt.server.json_paint_target import JsonPaintTarget
from muntjac.terminal.gwt.server.exceptions import ServletException
from muntjac.terminal.uri_handler import IErrorEvent as URIHandlerErrorEvent
from muntjac.terminal.terminal import IErrorEvent as TerminalErrorEvent
from muntjac.terminal.gwt.server.paste_wsgi_servlet import PasteWsgiServlet
from muntjac.terminal.gwt.server.exceptions import SessionExpiredException, SystemMessageException
from muntjac.terminal.gwt.client.application_connection import ApplicationConnection
from muntjac.terminal.gwt.server.web_application_context import WebApplicationContext
from muntjac.terminal.gwt.server.http_servlet_request_listener import IHttpServletRequestListener
from muntjac.terminal.parameter_handler import IErrorEvent as ParameterHandlerErrorEvent
logger = logging.getLogger(__name__)

class RequestType(object):
    FILE_UPLOAD = 'FILE_UPLOAD'
    UIDL = 'UIDL'
    OTHER = 'OTHER'
    STATIC_FILE = 'STATIC_FILE'
    APPLICATION_RESOURCE = 'APPLICATION_RESOURCE'
    _values = [
     FILE_UPLOAD, UIDL, OTHER, STATIC_FILE, APPLICATION_RESOURCE]

    @classmethod
    def values(cls):
        return cls._values[:]


class AbstractApplicationServlet(PasteWsgiServlet, Constants):
    """Abstract implementation of the ApplicationServlet which handles all
    communication between the client and the server.

    It is possible to extend this class to provide own functionality but in
    most cases this is unnecessary.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """
    VERSION = None
    VERSION_MAJOR = None
    VERSION_MINOR = None
    VERSION_REVISION = None
    VERSION_BUILD = None
    if '1.1.2' == '@VERSION@':
        VERSION = '9.9.9.INTERNAL-DEBUG-BUILD'
    else:
        VERSION = '1.1.2'
    digits = VERSION.split('.', 4)
    VERSION_MAJOR = int(digits[0])
    VERSION_MINOR = int(digits[1])
    VERSION_REVISION = int(digits[2])
    if len(digits) == 4:
        VERSION_BUILD = digits[3]
    else:
        VERSION_BUILD = ''
    REQUEST_FRAGMENT = ''
    REQUEST_VAADIN_STATIC_FILE_PATH = ''
    REQUEST_WIDGETSET = ''
    REQUEST_SHARED_WIDGETSET = ''
    REQUEST_DEFAULT_THEME = ''
    REQUEST_APPSTYLE = ''
    UPLOAD_URL_PREFIX = 'APP/UPLOAD/'

    def __init__(self, productionMode=False, debug=False, widgetset=None, resourceCacheTime=3600, disableXsrfProtection=False, *args, **kw_args):
        super(AbstractApplicationServlet, self).__init__(*args, **kw_args)
        self._applicationProperties = dict()
        self._productionMode = False
        self._resourcePath = None
        self._resourceCacheTime = 3600
        self._firstTransaction = True
        self._applicationProperties[self.SERVLET_PARAMETER_PRODUCTION_MODE] = 'true' if productionMode else 'false'
        self._applicationProperties[self.SERVLET_PARAMETER_DEBUG] = 'true' if debug else 'false'
        self._applicationProperties[self.PARAMETER_WIDGETSET] = self.DEFAULT_WIDGETSET if widgetset is None else widgetset
        self._applicationProperties[self.SERVLET_PARAMETER_RESOURCE_CACHE_TIME] = str(resourceCacheTime)
        self._applicationProperties[self.SERVLET_PARAMETER_DISABLE_XSRF_PROTECTION] = 'true' if disableXsrfProtection else 'false'
        return

    def init(self):
        """Called by the servlet container to indicate to a servlet that the
        servlet is being placed into service.
        """
        if self._firstTransaction:
            self._firstTransaction = False
            self.checkProductionMode()
            self.checkCrossSiteProtection()
            self.checkResourceCacheTime()

    def checkCrossSiteProtection(self):
        if self.getApplicationOrSystemProperty(self.SERVLET_PARAMETER_DISABLE_XSRF_PROTECTION, 'false') == 'true':
            logger.warning(self.WARNING_XSRF_PROTECTION_DISABLED)

    def checkWidgetsetVersion(self, request):
        """Checks that the version reported by the client (widgetset) matches
        that of the server.
        """
        if not self.VERSION == self.getParameter(request, 'wsver', ''):
            pass

    def checkProductionMode(self):
        """Check if the application is in production mode."""
        if self.getApplicationOrSystemProperty(self.SERVLET_PARAMETER_DEBUG, 'true') == 'false':
            self._productionMode = True
        elif self.getApplicationOrSystemProperty(self.SERVLET_PARAMETER_PRODUCTION_MODE, 'false') == 'true':
            self._productionMode = True
        if not self._productionMode:
            logger.warning(self.NOT_PRODUCTION_MODE_INFO)

    def checkResourceCacheTime(self):
        try:
            rct = self.getApplicationOrSystemProperty(self.SERVLET_PARAMETER_RESOURCE_CACHE_TIME, '3600')
            self._resourceCacheTime = int(rct)
        except ValueError:
            self._resourceCacheTime = 3600
            logger.warning(self.WARNING_RESOURCE_CACHING_TIME_NOT_NUMERIC)

    def getApplicationProperty(self, parameterName):
        """Gets an application property value.

        @param parameterName:
                   the Name or the parameter.
        @return: String value or C{None} if not found
        """
        val = self._applicationProperties.get(parameterName)
        if val is not None:
            return val
        else:
            val = self._applicationProperties.get(parameterName.lower())
            return val

    def getSystemProperty(self, parameterName):
        """Gets an system property value.

        @param parameterName:
                   the Name or the parameter.
        @return: String value or C{None} if not found
        """
        raise NotImplementedError

    def getApplicationOrSystemProperty(self, parameterName, defaultValue):
        """Gets an application or system property value.

        @param parameterName:
                   the Name or the parameter.
        @param defaultValue:
                   the Default to be used.
        @return: String value or default if not found
        """
        val = self.getApplicationProperty(parameterName)
        if val is not None:
            return val
        else:
            return defaultValue

    def isProductionMode(self):
        """Returns true if the servlet is running in production mode.
        Production mode disables all debug facilities.

        @return: true if in production mode, false if in debug mode
        """
        return self._productionMode

    def getResourceCacheTime(self):
        """Returns the amount of milliseconds the browser should cache a file.
        Default is 1 hour (3600 ms).

        @return: The amount of milliseconds files are cached in the browser
        """
        return self._resourceCacheTime

    def service(self, request, response):
        """Receives standard HTTP requests from the public service method and
        dispatches them.
        """
        requestType = self.getRequestType(request)
        if not self.ensureCookiesEnabled(requestType, request, response):
            return
        else:
            if requestType == RequestType.STATIC_FILE:
                self.serveStaticResources(request, response)
                return
            if self.isRepaintAll(request):
                self.checkWidgetsetVersion(request)
            application = None
            transactionStarted = False
            requestStarted = False
            try:
                try:
                    if requestType == RequestType.UIDL and ApplicationConnection.PARAM_UNLOADBURST in self.getParameters(request) and self.getContentLength(request) < 1 and self.getExistingApplication(request, False) is None:
                        self.redirectToApplication(request, response)
                        return
                    application = self.findApplicationInstance(request, requestType)
                    if application is None:
                        return
                    webApplicationContext = self.getApplicationContext(self.getSession(request))
                    applicationManager = webApplicationContext.getApplicationManager(application, self)
                    self.updateBrowserProperties(webApplicationContext.getBrowser(), request)
                    if isinstance(application, IHttpServletRequestListener):
                        application.onRequestStart(request, response)
                        requestStarted = True
                    self.startApplication(request, application, webApplicationContext)
                    webApplicationContext.startTransaction(application, request)
                    transactionStarted = True
                    if requestType == RequestType.FILE_UPLOAD:
                        applicationManager.handleFileUpload(request, response, self)
                        return
                    if requestType == RequestType.UIDL:
                        window = applicationManager.getApplicationWindow(request, self, application, None)
                        applicationManager.handleUidlRequest(request, response, self, window)
                        return
                    if not application.isRunning():
                        self.endApplication(request, response, application)
                        return
                    window = self.getApplicationWindow(request, applicationManager, application)
                    if window is None:
                        raise ServletException(self.ERROR_NO_WINDOW_FOUND)
                    if window.getTerminal() is None:
                        window.setTerminal(webApplicationContext.getBrowser())
                    parameters = request.fields()
                    if window is not None and parameters is not None:
                        window.handleParameters(parameters)
                    if self.handleURI(applicationManager, window, request, response):
                        return
                    self.writeAjaxPage(request, response, window, application)
                except SessionExpiredException as e:
                    self.handleServiceSessionExpired(request, response)

            finally:
                try:
                    if transactionStarted:
                        application.getContext().endTransaction(application, request)
                finally:
                    if requestStarted:
                        application.onRequestEnd(request, response)

            return

    def ensureCookiesEnabled(self, requestType, request, response):
        """Check that cookie support is enabled in the browser. Only checks
        UIDL requests.

        @param requestType:
                   Type of the request as returned by L{getRequestType}
        @param request:
                   The request from the browser
        @param response:
                   The response to which an error can be written
        @return: false if cookies are disabled, true otherwise
        @raise IOException:
        """
        if requestType == RequestType.UIDL and not self.isRepaintAll(request):
            if self.getSessionId(request) is None:
                self.criticalNotification(request, response, self.getSystemMessages().getCookiesDisabledCaption(), self.getSystemMessages().getCookiesDisabledMessage(), None, self.getSystemMessages().getCookiesDisabledURL())
                return False
        return True

    def updateBrowserProperties(self, browser, request):
        browser.updateRequestDetails(self.getLocale(request), self.getHeader(request, 'REMOTE_ADDR'), self.isSecure(request), self.getUserAgent(request))
        if request.field('repaintAll', None) is not None:
            browser.updateClientSideDetails(self.getParameter(request, 'sw', None), self.getParameter(request, 'sh', None), self.getParameter(request, 'tzo', None), self.getParameter(request, 'rtzo', None), self.getParameter(request, 'dstd', None), self.getParameter(request, 'dston', None), self.getParameter(request, 'curdate', None), self.getParameter(request, 'td', None) is not None)
        return

    def criticalNotification(self, request, response, caption, message, details, url):
        """Send a notification to client's application. Used to notify
        client of critical errors, session expiration and more. Server
        has no knowledge of what application client refers to.

        @param request:
                   the HTTP request instance.
        @param response:
                   the HTTP response to write to.
        @param caption:
                   the notification caption
        @param message:
                   to notification body
        @param details:
                   a detail message to show in addition to the message.
                   Currently shown directly below the message but could be
                   hidden behind a details drop down in the future. Mainly
                   used to give additional information not necessarily
                   useful to the end user.
        @param url:
                   url to load when the message is dismissed. Null will
                   reload the current page.
        @raise IOException:
                    if the writing failed due to input/output error.
        """
        if self.isUIDLRequest(request):
            if caption is not None:
                caption = '"' + JsonPaintTarget.escapeJSON(caption) + '"'
            if details is not None:
                if message is None:
                    message = details
                else:
                    message += '<br/><br/>' + details
            if message is not None:
                message = '"' + JsonPaintTarget.escapeJSON(message) + '"'
            else:
                message = 'null'
            if url is not None:
                url = '"' + JsonPaintTarget.escapeJSON(url) + '"'
            else:
                url = 'null'
            output = 'for(;;);[{"changes":[], "meta" : {"appError": {' + '"caption":' + caption + ',"message" : ' + message + ',' + '"url" : ' + url + '}}, "resources": {}, "locales":[]}]'
            self.writeResponse(response, 'application/json; charset=UTF-8', output)
        else:
            output = ''
            if url is not None:
                output += '<a href="' + url + '">'
            if caption is not None:
                output += '<b>' + caption + '</b><br/>'
            if message is not None:
                output += message
                output += '<br/><br/>'
            if details is not None:
                output += details
                output += '<br/><br/>'
            if url is not None:
                output += '</a>'
            self.writeResponse(response, 'text/html; charset=UTF-8', output)
        return

    def writeResponse(self, response, contentType, output):
        """Writes the response in C{output} using the contentType given
        in C{contentType} to the provided L{HttpServletResponse}

        @param response:
        @param contentType:
        @param output:
                   Output to write (UTF-8 encoded)
        @raise IOException:
        """
        self.setHeader(response, 'Content-Type', contentType)
        self.write(response, output)

    def findApplicationInstance(self, request, requestType):
        """Returns the application instance to be used for the request. If
        an existing instance is not found a new one is created or null is
        returned to indicate that the application is not available.

        @raise ServletException:
        @raise SessionExpiredException:
        """
        requestCanCreateApplication = self.requestCanCreateApplication(request, requestType)
        application = self.getExistingApplication(request, requestCanCreateApplication)
        if application is not None:
            restartApplication = self.getParameter(request, self.URL_PARAMETER_RESTART_APPLICATION, None) is not None
            closeApplication = self.getParameter(request, self.URL_PARAMETER_CLOSE_APPLICATION, None) is not None
            if restartApplication:
                session = self.getSession(request, False)
                self.closeApplication(application, session)
                return self.createApplication(request)
            if closeApplication:
                session = self.getSession(request, False)
                self.closeApplication(application, session)
                return
            return application
        if requestCanCreateApplication:
            return self.createApplication(request)
        else:
            raise SessionExpiredException()
            return

    def requestCanCreateApplication(self, request, requestType):
        """Check if the request should create an application if an existing
        application is not found.

        @return: true if an application should be created, false otherwise
        """
        if requestType == RequestType.UIDL and self.isRepaintAll(request):
            return True
        if requestType == RequestType.OTHER:
            return True
        return False

    def handleDownload(self, stream, request, response):
        """Handles the requested URI. An application can add handlers to do
        special processing, when a certain URI is requested. The handlers
        are invoked before any windows URIs are processed and if a
        DownloadStream is returned it is sent to the client.

        @param stream:
                   the download stream.
        @param request:
                   the HTTP request instance.
        @param response:
                   the HTTP response to write to.
        @raise IOException:

        @see: L{URIHandler}
        """
        if stream.getParameter('Location') is not None:
            self.setStatus(response, 302, 'Found')
            self.setHeader(response, 'Location', stream.getParameter('Location'))
            return
        data = stream.getStream()
        if data is not None:
            self.setHeader(response, 'Content-Type', stream.getContentType())
            cacheTime = stream.getCacheTime()
            if cacheTime <= 0:
                self.setHeader(response, 'Cache-Control', 'no-cache')
                self.setHeader(response, 'Pragma', 'no-cache')
                self.setHeader(response, 'Expires', '0')
            else:
                self.setHeader(response, 'Cache-Control', 'max-age=' + str(cacheTime / 1000))
                self.setHeader(response, 'Expires', str(1000 * time() + cacheTime))
                self.setHeader(response, 'Pragma', 'cache')
            names = stream.getParameterNames()
            if names is not None:
                for param in names:
                    self.setHeader(response, param, stream.getParameter(param))

            contentDispositionValue = stream.getParameter('Content-Disposition')
            if contentDispositionValue is None:
                contentDispositionValue = 'filename="' + stream.getFileName() + '"'
                self.setHeader(response, 'Content-Disposition', contentDispositionValue)
            self.write(response, data.getvalue())
            data.close()
        return

    def createApplication(self, request):
        """Creates a new application and registers it into
        WebApplicationContext (aka session). This is not meant to be
        overridden. Override getNewApplication to create the application
        instance in a custom way.

        @raise ServletException:
        @raise MalformedURLException:
        """
        newApplication = self.getNewApplication(request)
        context = self.getApplicationContext(self.getSession(request))
        context.addApplication(newApplication)
        return newApplication

    def handleServiceException(self, request, response, application, e):
        if self.getRequestType(request) == RequestType.UIDL:
            ci = self.getSystemMessages()
            self.criticalNotification(request, response, ci.getInternalErrorCaption(), ci.getInternalErrorMessage(), None, ci.getInternalErrorURL())
            if application is not None:
                application.getErrorHandler().terminalError(RequestError(e))
            else:
                raise ServletException(e)
        else:
            raise ServletException, str(e)
        return

    def getThemeForWindow(self, request, window):
        """Returns the theme for given request/window
        """
        if self.getParameter(request, self.URL_PARAMETER_THEME, None) is not None:
            themeName = self.getParameter(request, self.URL_PARAMETER_THEME)
        else:
            themeName = window.getTheme()
        if themeName is None:
            if self.getParameter(request, self.REQUEST_DEFAULT_THEME, None) is not None:
                themeName = self.getParameter(request, self.REQUEST_DEFAULT_THEME)
            else:
                themeName = self.getDefaultTheme()
        themeName = self.stripSpecialChars(themeName)
        return themeName

    @classmethod
    def stripSpecialChars(cls, themeName):
        """A helper method to strip away characters that might somehow be
        used for XSS attacks. Leaves at least alphanumeric characters intact.
        Also removes eg. ( and ), so values should be safe in javascript too.
        """
        sb = StringIO()
        for c in themeName:
            if c not in cls._CHAR_BLACKLIST:
                sb.write(c)

        result = sb.getvalue()
        sb.close()
        return result

    _CHAR_BLACKLIST = [
     '&', '"', "'", '<', '>', '(', ')', ';']

    @classmethod
    def getDefaultTheme(cls):
        """Returns the default theme. Must never return C{None}.
        """
        return cls.DEFAULT_THEME_NAME

    def handleURI(self, applicationManager, window, request, response):
        """Calls URI handlers for the request. If an URI handler returns a
        DownloadStream the stream is passed to the client for downloading.

        @return: true if an DownloadStream was sent to the client
        @raise IOException
        """
        download = applicationManager.handleURI(window, request, response, self)
        if download is not None:
            self.handleDownload(download, request, response)
            return True
        else:
            return False

    def handleServiceSessionExpired(self, request, response):
        if self.isOnUnloadRequest(request):
            return
        else:
            try:
                ci = self.getSystemMessages()
                if self.getRequestType(request) != RequestType.UIDL:
                    response.sendRedirect(ci.getSessionExpiredURL())
                else:
                    self.invalidateSession(request)
                    self.criticalNotification(request, response, ci.getSessionExpiredCaption(), ci.getSessionExpiredMessage(), None, ci.getSessionExpiredURL())
            except SystemMessageException as ee:
                raise ServletException(ee)

            return

    def handleServiceSecurityException(self, request, response):
        if self.isOnUnloadRequest(request):
            return
        try:
            ci = self.getSystemMessages()
            if self.getRequestType(request) != RequestType.UIDL:
                self.redirect(response, ci.getCommunicationErrorURL())
            else:
                self.criticalNotification(request, response, ci.getCommunicationErrorCaption(), ci.getCommunicationErrorMessage(), self.INVALID_SECURITY_KEY_MSG, ci.getCommunicationErrorURL())
                self.invalidateSession(request)
        except SystemMessageException as ee:
            raise ServletException(ee)

        logger.error('Invalid security key received from ' + request.getRemoteHost())

    def getNewApplication(self, request):
        """Creates a new application for the given request.

        @param request:
                   the HTTP request.
        @return: A new Application instance.
        @raise ServletException:
        """
        raise NotImplementedError

    def startApplication(self, request, application, webApplicationContext):
        """Starts the application if it is not already running.

        @raise ServletException:
        @raise MalformedURLException:
        """
        if not application.isRunning():
            applicationUrl = self.getApplicationUrl(request)
            lc = self.getLocale(request)
            application.setLocale(lc)
            application.start(applicationUrl, self._applicationProperties, webApplicationContext)

    def serveStaticResources(self, request, response):
        """Check if this is a request for a static resource and, if it is,
        serve the resource to the client.

        @return: true if a file was served and the request has been handled,
                 false otherwise.
        @raise IOException:
        @raise ServletException:
        """
        pathInfo = self.getPathInfo(request)
        if pathInfo is None or len(pathInfo) <= 10:
            return False
        contextPath = self.getContextPath(request)
        if contextPath is not None and self.getRequestUri(request).startswith('/VAADIN/'):
            self.serveStaticResourcesInVAADIN(self.getRequestUri(request), request, response)
            return True
        else:
            if self.getRequestUri(request).startswith(contextPath + '/VAADIN/'):
                self.serveStaticResourcesInVAADIN(self.getRequestUri(request)[len(contextPath):], request, response)
                return True
            return False

    def serveStaticResourcesInVAADIN(self, filename, request, response):
        """Serve resources from VAADIN directory.

        @param filename:
                   The filename to serve. Should always start with /VAADIN/.
        @param request:
        @param response:
        @raise IOException:
        @raise ServletException:
        """
        resourceUrl = self.getResource(filename)
        if not exists(resourceUrl):
            msg = 'Requested resource [' + filename + '] not found'
            logger.info(msg)
            self.setStatus(response, 404, msg)
            return
        else:
            if not self.isAllowedVAADINResourceUrl(request, resourceUrl):
                msg = 'Requested resource [%s] not accessible in the VAADIN directory or access to it is forbidden.' % filename
                logger.info(msg)
                self.setStatus(response, 403, msg)
                return
            lastModifiedTime = 0
            try:
                lastModifiedTime = int(getmtime(resourceUrl) * 1000)
                lastModifiedTime = lastModifiedTime - lastModifiedTime % 1000
                if self.browserHasNewestVersion(request, lastModifiedTime):
                    self.setStatus(response, 304, 'Not Modified')
                    return
            except Exception:
                logger.info('Failed to find out last modified timestamp. ' + 'Continuing without it.')

            mimetype, _ = mimetypes.guess_type(filename)
            if mimetype is not None:
                self.setHeader(response, 'Content-Type', mimetype)
            if lastModifiedTime > 0:
                self.setHeader(response, 'Last-Modified', str(lastModifiedTime))
                self.setHeader(response, 'Cache-Control', 'max-age: ' + str(self._resourceCacheTime))
            fd = open(resourceUrl, 'rb')
            self.write(response, fd.read())
            fd.close()
            return

    def isAllowedVAADINResourceUrl(self, request, resourceUrl):
        """Check whether a URL obtained from a classloader refers to a valid
        static resource in the directory VAADIN.

        Warning: Overriding of this method is not recommended, but is possible
        to support non-default classloaders or servers that may produce URLs
        different from the normal ones. The method prototype may change in the
        future. Care should be taken not to expose class files or other
        resources outside the VAADIN directory if the method is overridden.
        """
        if '/VAADIN/' not in self.getUrlPath(resourceUrl) or '/../' in self.getUrlPath(resourceUrl):
            logger.info('Blocked attempt to access file: ' + resourceUrl)
            return False
        return True

    def browserHasNewestVersion(self, request, resourceLastModifiedTimestamp):
        """Checks if the browser has an up to date cached version of
        requested resource. Currently the check is performed using the
        "If-Modified-Since" header. Could be expanded if needed.

        @param request:
                   The HttpServletRequest from the browser.
        @param resourceLastModifiedTimestamp:
                   The timestamp when the resource was last modified. 0 if
                   the last modification time is unknown.
        @return: true if the If-Modified-Since header tells the cached version
                    in the browser is up to date, false otherwise
        """
        if resourceLastModifiedTimestamp < 1:
            return False
        try:
            headerIfModifiedSince = self.getIfModifiedSince(request)
            if headerIfModifiedSince >= resourceLastModifiedTimestamp:
                return True
        except Exception:
            pass

        return False

    def getRequestType(self, request):
        if self.isFileUploadRequest(request):
            return RequestType.FILE_UPLOAD
        else:
            if self.isUIDLRequest(request):
                return RequestType.UIDL
            if self.isStaticResourceRequest(request):
                return RequestType.STATIC_FILE
            if self.isApplicationRequest(request):
                return RequestType.APPLICATION_RESOURCE
            if self.getParameter(request, 'FileId', None) is not None:
                return RequestType.FILE_UPLOAD
            return RequestType.OTHER

    def isApplicationRequest(self, request):
        path = self.getRequestPathInfo(request)
        if path is not None and path.startswith('/APP/'):
            return True
        else:
            return False

    def isStaticResourceRequest(self, request):
        pathInfo = self.getPathInfo(request)
        if pathInfo is None or len(pathInfo) <= 10:
            return False
        contextPath = self.getContextPath(request)
        if contextPath is not None and self.getRequestUri(request).startswith('/VAADIN/'):
            return True
        else:
            if self.getRequestUri(request).startswith(contextPath + '/VAADIN/'):
                return True
            return False

    def isUIDLRequest(self, request):
        pathInfo = self.getRequestPathInfo(request)
        if pathInfo is None:
            return False
        else:
            compare = self.AJAX_UIDL_URI
            if pathInfo.startswith(compare + '/') or pathInfo.endswith(compare):
                return True
            return False

    def isFileUploadRequest(self, request):
        pathInfo = self.getRequestPathInfo(request)
        if pathInfo is None:
            return False
        else:
            if pathInfo.startswith('/' + self.UPLOAD_URL_PREFIX):
                return True
            return False

    def isOnUnloadRequest(self, request):
        param = ApplicationConnection.PARAM_UNLOADBURST
        return self.getParameter(request, param, None) is not None

    def getSystemMessages(self):
        """Get system messages from the current application class
        """
        try:
            appCls = self.getApplicationClass()
            return appCls.getSystemMessages()
        except AttributeError:
            raise SystemMessageException('Application.getSystemMessage() should be callable')

        return Application.getSystemMessages()

    def getApplicationClass(self):
        raise NotImplementedError

    def getStaticFilesLocation(self, request):
        """Return the URL from where static files, e.g. the widgetset and
        the theme, are served. In a standard configuration the VAADIN folder
        inside the returned folder is what is used for widgetsets and themes.

        The returned folder is usually the same as the context path and
        independent of the application.

        @return: The location of static resources (should contain the VAADIN
                directory). Never ends with a slash (/).
        """
        param = self.REQUEST_VAADIN_STATIC_FILE_PATH
        staticFileLocation = self.getParameter(request, param)
        if staticFileLocation is not None:
            return staticFileLocation
        else:
            return self.getWebApplicationsStaticFileLocation(request)

    def getWebApplicationsStaticFileLocation(self, request):
        """The default method to fetch static files location (URL). This
        method does not check for request attribute
        C{REQUEST_VAADIN_STATIC_FILE_PATH}.
        """
        staticFileLocation = self.getApplicationOrSystemProperty(self.PARAMETER_VAADIN_RESOURCES, None)
        if staticFileLocation is not None:
            return staticFileLocation
        else:
            ctxPath = self.getContextPath(request)
            if len(ctxPath) == 0 and self.originalContextPath(request) is not None:
                ctxPath = self.originalContextPath(request)
            ctxPath = self.removeHeadingOrTrailing(ctxPath, '/')
            if ctxPath == '':
                return ''
            return '/' + ctxPath
            return

    @classmethod
    def removeHeadingOrTrailing(cls, string, what):
        """Remove any heading or trailing "what" from the "string".
        """
        while string.startswith(what):
            string = string[1:]

        while string.endswith(what):
            string = string[:-1]

        return string

    def redirectToApplication(self, request, response):
        """Write a redirect response to the main page of the application.

        @raise IOException:
                    if sending the redirect fails due to an input/output
                    error or a bad application URL
        """
        applicationUrl = self.getApplicationUrl(request)
        self.sendRedirect(response, applicationUrl)

    def writeAjaxPage(self, request, response, window, application):
        """This method writes the html host page (aka kickstart page) that
        starts the actual Muntjac application.

        If one needs to override parts of the host page, it is suggested
        that one overrides on of several submethods which are called by
        this method:

          - L{setAjaxPageHeaders}
          - L{writeAjaxPageHtmlHeadStart}
          - L{writeAjaxPageHtmlHeader}
          - L{writeAjaxPageHtmlBodyStart}
          - L{writeAjaxPageHtmlMuntjacScripts}
          - L{writeAjaxPageHtmlMainDiv}
          - L{writeAjaxPageHtmlBodyEnd}

        @param request:
                   the HTTP request.
        @param response:
                   the HTTP response to write to.
        @param window:
        @param application:
        @raise IOException:
                    if the writing failed due to input/output error.
        @raise MalformedURLException:
                    if the application is denied access the persistent data
                    store represented by the given URL.
        """
        fragment = self.getParameter(request, self.REQUEST_FRAGMENT, None) is not None
        if fragment:
            self.setParameter(request, clsname(Application), application)
        page = StringIO()
        if window.getCaption() is None:
            title = 'Muntjac 6'
        else:
            title = window.getCaption()
        appUrl = self.getUrlPath(self.getApplicationUrl(request))
        if appUrl.endswith('/'):
            appUrl = appUrl[:-1]
        themeName = self.getThemeForWindow(request, window)
        themeUri = self.getThemeUri(themeName, request)
        if not fragment:
            self.setAjaxPageHeaders(response)
            self.writeAjaxPageHtmlHeadStart(page, request)
            self.writeAjaxPageHtmlHeader(page, title, themeUri, request)
            self.writeAjaxPageHtmlBodyStart(page, request)
        appId = appUrl
        if '' == appUrl:
            appId = 'ROOT'
        appId = re.sub('[^a-zA-Z0-9]', '', appId)
        hashCode = hash(appId)
        if hashCode < 0:
            hashCode = -hashCode
        appId = appId + '-' + str(hashCode)
        self.writeAjaxPageHtmlMuntjacScripts(window, themeName, application, page, appUrl, themeUri, appId, request)
        appClass = 'v-app-' + self.getApplicationCSSClassName()
        themeClass = ''
        if themeName is not None:
            themeClass = 'v-theme-' + re.sub('[^a-zA-Z0-9]', '', themeName)
        else:
            themeClass = 'v-theme-' + re.sub('[^a-zA-Z0-9]', '', self.getDefaultTheme())
        classNames = 'v-app ' + themeClass + ' ' + appClass
        divStyle = None
        if self.getParameter(request, self.REQUEST_APPSTYLE, None) is not None:
            divStyle = 'style="' + self.getParameter(request, self.REQUEST_APPSTYLE) + '"'
        self.writeAjaxPageHtmlMainDiv(page, appId, classNames, divStyle, request)
        if not fragment:
            page.write('</body>\n</html>\n')
        self.write(response, page.getvalue())
        page.close()
        return

    def getApplicationCSSClassName(self):
        """Returns the application class identifier for use in the
        application CSS class name in the root DIV. The application
        CSS class name is of form "v-app-"+getApplicationCSSClassName().

        This method should normally not be overridden.

        @return: The CSS class name to use in combination with "v-app-".
        """
        try:
            return self.getApplicationClass().__name__
        except Exception as e:
            logger.warning('getApplicationCSSClassName failed')
            return 'unknown'

    def getThemeUri(self, themeName, request):
        """Get the URI for the application theme.

        A portal-wide default theme is fetched from the portal shared
        resource directory (if any), other themes from the portlet.
        """
        if themeName == self.getParameter(request, self.REQUEST_DEFAULT_THEME, None):
            staticFilePath = self.getStaticFilesLocation(request)
        else:
            staticFilePath = self.getWebApplicationsStaticFileLocation(request)
        return staticFilePath + '/' + self.THEME_DIRECTORY_PATH + themeName

    def writeAjaxPageHtmlMainDiv(self, page, appId, classNames, divStyle, request):
        """Method to write the div element into which that actual Muntjac
        application is rendered.

        Override this method if you want to add some custom html around around
        the div element into which the actual Muntjac application will be
        rendered.

        @raise IOException:
        """
        page.write('<div id="' + appId + '" class="' + classNames + '" ' + (divStyle if divStyle is not None else '') + '>')
        page.write('<div class="v-app-loading"></div>')
        page.write('</div>\n')
        page.write('<noscript>' + self.getNoScriptMessage() + '</noscript>')
        return

    def writeAjaxPageHtmlMuntjacScripts(self, window, themeName, application, page, appUrl, themeUri, appId, request):
        """Method to write the script part of the page which loads needed
        Muntjac scripts and themes.

        Override this method if you want to add some custom html around
        scripts.

        @raise ServletException:
        @raise IOException:
        """
        requestWidgetset = self.getParameter(request, self.REQUEST_WIDGETSET, None)
        sharedWidgetset = self.getParameter(request, self.REQUEST_SHARED_WIDGETSET, None)
        if requestWidgetset is None and sharedWidgetset is None:
            requestWidgetset = self.getApplicationOrSystemProperty(self.PARAMETER_WIDGETSET, self.DEFAULT_WIDGETSET)
        if requestWidgetset is not None:
            widgetset = requestWidgetset
            widgetsetBasePath = self.getWebApplicationsStaticFileLocation(request)
        else:
            widgetset = sharedWidgetset
            widgetsetBasePath = self.getStaticFilesLocation(request)
        widgetset = self.stripSpecialChars(widgetset)
        widgetsetFilePath = widgetsetBasePath + '/' + self.WIDGETSET_DIRECTORY_PATH + widgetset + '/' + widgetset + '.nocache.js?' + str(int(time() * 1000))
        systemMessages = None
        try:
            systemMessages = self.getSystemMessages()
        except SystemMessageException as e:
            raise ServletException('CommunicationError!', e)

        page.write('<script type="text/javascript">\n')
        page.write('//<![CDATA[\n')
        page.write('if(!vaadin || !vaadin.vaadinConfigurations) {\n ' + 'if(!vaadin) { var vaadin = {}} \n' + 'vaadin.vaadinConfigurations = {};\n' + 'if (!vaadin.themesLoaded) ' + '{ vaadin.themesLoaded = {}; }\n')
        if not self.isProductionMode():
            page.write('vaadin.debug = true;\n')
        page.write('document.write(\'<iframe tabIndex="-1" ' + 'id="__gwt_historyFrame" ' + 'style="position:absolute;width:0;height:0;border:0;' + 'overflow:hidden;" ' + 'src="javascript:false"></iframe>\');\n')
        page.write('document.write("<script language=\'javascript\' ' + "src='" + widgetsetFilePath + '\'><\\/script>");\n}\n')
        page.write('vaadin.vaadinConfigurations["' + appId + '"] = {')
        page.write("appUri:'" + appUrl + "', ")
        if window != application.getMainWindow():
            page.write('windowName: "' + JsonPaintTarget.escapeJSON(window.getName()) + '", ')
        if self.isStandalone():
            page.write('standalone: true, ')
        page.write('themeUri:')
        page.write('"' + themeUri + '"' if themeUri is not None else 'null')
        page.write(', versionInfo : {vaadinVersion:"')
        page.write(self.VERSION)
        page.write('",applicationVersion:"')
        page.write(JsonPaintTarget.escapeJSON(application.getVersion()))
        page.write('"}')
        if systemMessages is not None:
            caption = systemMessages.getCommunicationErrorCaption()
            if caption is not None:
                caption = '"' + JsonPaintTarget.escapeJSON(caption) + '"'
            message = systemMessages.getCommunicationErrorMessage()
            if message is not None:
                message = '"' + JsonPaintTarget.escapeJSON(message) + '"'
            url = systemMessages.getCommunicationErrorURL()
            if url is not None:
                url = '"' + JsonPaintTarget.escapeJSON(url) + '"'
            else:
                url = 'null'
            page.write(',"comErrMsg": {' + '"caption":' + caption + ',' + '"message" : ' + message + ',' + '"url" : ' + url + '}')
            caption = systemMessages.getAuthenticationErrorCaption()
            if caption is not None:
                caption = '"' + JsonPaintTarget.escapeJSON(caption) + '"'
            message = systemMessages.getAuthenticationErrorMessage()
            if message is not None:
                message = '"' + JsonPaintTarget.escapeJSON(message) + '"'
            url = systemMessages.getAuthenticationErrorURL()
            if url is not None:
                url = '"' + JsonPaintTarget.escapeJSON(url) + '"'
            else:
                url = 'null'
            page.write(',"authErrMsg": {' + '"caption":' + caption + ',' + '"message" : ' + message + ',' + '"url" : ' + url + '}')
        page.write('};\n//]]>\n</script>\n')
        if themeName is not None:
            page.write('<script type="text/javascript">\n')
            page.write('//<![CDATA[\n')
            page.write("if(!vaadin.themesLoaded['" + themeName + "']) {\n")
            page.write("var stylesheet = document.createElement('link');\n")
            page.write("stylesheet.setAttribute('rel', 'stylesheet');\n")
            page.write("stylesheet.setAttribute('type', 'text/css');\n")
            page.write("stylesheet.setAttribute('href', '" + themeUri + "/styles.css');\n")
            page.write("document.getElementsByTagName('head')[0].appendChild(stylesheet);\n")
            page.write("vaadin.themesLoaded['" + themeName + "'] = true;\n}\n")
            page.write('//]]>\n</script>\n')
        page.write('<script type="text/javascript">\n')
        page.write('//<![CDATA[\n')
        page.write("setTimeout('if (typeof " + widgetset.replace('.', '_') + ' == "undefined") {alert("Failed to load the widgetset: ' + widgetsetFilePath + '")};\',15000);\n' + '//]]>\n</script>\n')
        return

    def isStandalone(self):
        """@return: true if the served application is considered to be the
                only or main content of the host page. E.g. various embedding
                solutions should override this to false.
        """
        return True

    def writeAjaxPageHtmlBodyStart(self, page, request):
        """Method to open the body tag of the html kickstart page.

        This method is responsible for closing the head tag and opening
        the body tag.

        Override this method if you want to add some custom html to the page.

        @raise IOException:
        """
        page.write('\n</head>\n<body scroll="auto" class="' + ApplicationConnection.GENERATED_BODY_CLASSNAME + '">\n')

    def writeAjaxPageHtmlHeader(self, page, title, themeUri, request):
        """Method to write the contents of head element in html kickstart page.

        Override this method if you want to add some custom html to the header
        of the page.

        @raise IOException:
        """
        page.write('<meta http-equiv="Content-Type" ' + 'content="text/html; charset=utf-8"/>\n')
        context = self.getApplicationContext(self.getSession(request))
        browser = context.getBrowser()
        if browser.isIE():
            page.write('<meta http-equiv="X-UA-Compatible" ' + 'content="chrome=1"/>\n')
        page.write('<style type="text/css">' + 'html, body {height:100%;margin:0;}</style>')
        page.write('<link rel="shortcut icon" ' + 'type="image/vnd.microsoft.icon" href="' + themeUri + '/favicon.ico" />')
        page.write('<link rel="icon" type="image/vnd.microsoft.icon" ' + 'href="' + themeUri + '/favicon.ico" />')
        page.write('<title>' + self.safeEscapeForHtml(title) + '</title>')

    def writeAjaxPageHtmlHeadStart(self, page, request):
        """Method to write the beginning of the html page.

        This method is responsible for writing appropriate doc type
        declarations and to open html and head tags.

        Override this method if you want to add some custom html to the
        very beginning of the page.

        @raise IOException:
        """
        page.write('<!DOCTYPE html PUBLIC "-//W3C//DTD ' + 'XHTML 1.0 Transitional//EN" ' + '"http://www.w3.org/TR/xhtml1/' + 'DTD/xhtml1-transitional.dtd">\n')
        page.write('<html xmlns="http://www.w3.org/1999/xhtml"' + '>\n<head>\n')

    def setAjaxPageHeaders(self, response):
        """Method to set http request headers for the Muntjac kickstart page.

        Override this method if you need to customize http headers of the page.
        """
        self.setHeader(response, 'Cache-Control', 'no-cache')
        self.setHeader(response, 'Pragma', 'no-cache')
        self.setHeader(response, 'Expires', '0')
        self.setHeader(response, 'Content-Type', 'text/html; charset=UTF-8')

    def getNoScriptMessage(self):
        """Returns a message printed for browsers without scripting support
        or if browsers scripting support is disabled.
        """
        return 'You have to enable javascript in your browser to use an application built with Muntjac.'

    def getApplicationUrl(self, request):
        """Gets the current application URL from request.

        @param request:
                   the HTTP request.
        @raise MalformedURLException:
                    if the application is denied access to the persistent
                    data store represented by the given URL.
        """
        reqURL = 'https://' if self.isSecure(request) else 'http://'
        reqHost = request.environ().get('HTTP_HOST')
        if reqHost:
            reqURL += reqHost
        else:
            reqURL += self.getServerName(request)
            if self.isSecure(request) and self.getServerPort(request) == 443 or not self.isSecure(request) and self.getServerPort(request) == 80:
                pass
            else:
                reqURL += ':%d' % self.getServerPort(request)
        reqURL += self.getRequestUri(request)
        if self.getParameter(request, 'javax.servlet.include.servlet_path', None) is not None:
            servletPath = self.getParameter(request, 'javax.servlet.include.context_path', None) + self.getParameter(request, 'javax.servlet.include.servlet_path', None)
        else:
            servletPath = self.getContextPath(request) + self.getServletPath(request)
        if len(servletPath) == 0 or servletPath[(len(servletPath) - 1)] != '/':
            servletPath = servletPath + '/'
        return urljoin(reqURL, servletPath)

    def getExistingApplication(self, request, allowSessionCreation):
        """Gets the existing application for given request. Looks for
        application instance for given request based on the requested URL.

        @param request:
                   the HTTP request.
        @param allowSessionCreation:
                   true if a session should be created if no session
                   exists, false if no session should be created
        @return: Application instance, or null if the URL does not map to
                    valid application.
        @raise MalformedURLException:
                    if the application is denied access to the persistent
                    data store represented by the given URL.
        @raise SessionExpiredException:
        """
        session = self.getSession(request, allowSessionCreation)
        if session is None:
            raise SessionExpiredException()
        context = self.getApplicationContext(session)
        applications = context.getApplications()
        for sessionApplication in applications:
            sessionApplicationPath = self.getUrlPath(sessionApplication.getURL())
            requestApplicationPath = self.getUrlPath(self.getApplicationUrl(request))
            if requestApplicationPath == sessionApplicationPath:
                if sessionApplication.isRunning():
                    return sessionApplication
                self.getApplicationContext(session).removeApplication(sessionApplication)
                break

        return

    def endApplication(self, request, response, application):
        """Ends the application.

        @param request:
                   the HTTP request.
        @param response:
                   the HTTP response to write to.
        @param application:
                   the application to end.
        @raise IOException:
                    if the writing failed due to input/output error.
        """
        logoutUrl = application.getLogoutURL()
        if logoutUrl is None:
            logoutUrl = application.getURL()
        session = self.getSession(request)
        if session is not None:
            self.getApplicationContext(session).removeApplication(application)
        response.sendRedirect(logoutUrl)
        return

    def getApplicationWindow(self, request, applicationManager, application):
        """Gets the existing application or create a new one. Get a
        window within an application based on the requested URI.

        @param request:
                   the HTTP Request.
        @param application:
                   the Application to query for window.
        @return: Window matching the given URI or null if not found.
        @raise ServletException:
                    if an exception has occurred that interferes with the
                    servlet's normal operation.
        """
        assumedWindow = None
        path = self.getRequestPathInfo(request)
        if not (path is None or len(path) == 0 or path == '/'):
            if path.startswith('/APP/'):
                return application.getMainWindow()
            windowName = None
            if path[0] == '/':
                path = path[1:]
            index = path.find('/')
            if index < 0:
                windowName = path
                path = ''
            else:
                windowName = path[:index]
            assumedWindow = application.getWindow(windowName)
        return applicationManager.getApplicationWindow(request, self, application, assumedWindow)

    def getRequestPathInfo(self, request):
        """Returns the path info; note that this _can_ be different than
        request.getPathInfo(). Examples where this might be useful:

          - An application runner servlet that runs different Muntjac
            applications based on an identifier.
          - Providing a REST interface in the context root, while serving a
            Muntjac UI on a sub-URI using only one servlet (e.g. REST on
            http://example.com/foo, UI on http://example.com/foo/vaadin)
        """
        return self.getPathInfo(request)

    def getResourceLocation(self, theme, resource):
        """Gets relative location of a theme resource.

        @param theme:
                   the Theme name.
        @param resource:
                   the Theme resource.
        @return: External URI specifying the resource
        """
        if self._resourcePath is None:
            return resource.getResourceId()
        else:
            return self._resourcePath + theme + '/' + resource.getResourceId()

    def isRepaintAll(self, request):
        return self.getParameter(request, self.URL_PARAMETER_REPAINT_ALL, None) is not None and self.getParameter(request, self.URL_PARAMETER_REPAINT_ALL, '') == '1'

    def closeApplication(self, application, session):
        if application is None:
            return
        else:
            application.close()
            if session is not None:
                context = self.getApplicationContext(session)
                context.removeApplication(application)
            return

    def getApplicationContext(self, session):
        """Gets the application context from an HttpSession. If no context
        is currently stored in a session a new context is created and stored
        in the session.

        @param session:
                   the HTTP session.
        @return: the application context for HttpSession.
        """
        return WebApplicationContext.getApplicationContext(session, self)

    def createCommunicationManager(self, application):
        """Override this method if you need to use a specialized
        communication mananger implementation.

        @deprecated: Instead of overriding this method, override
                    L{WebApplicationContext} implementation via
                    L{getApplicationContext} method and in that customized
                    implementation return your CommunicationManager in
                    L{WebApplicationContext.getApplicationManager}
                    method.
        """
        warn('deprecated', DeprecationWarning)
        from muntjac.terminal.gwt.server.communication_manager import CommunicationManager
        return CommunicationManager(application)

    @classmethod
    def safeEscapeForHtml(cls, unsafe):
        """Escapes characters to html entities. An exception is made for some
        "safe characters" to keep the text somewhat readable.

        @return: a safe string to be added inside an html tag
        """
        if unsafe is None:
            return
        else:
            safe = StringIO()
            for c in unsafe:
                if cls.isSafe(ord(c)):
                    safe.write(c)
                else:
                    safe.write('&#')
                    safe.write(ord(c))
                    safe.write(';')

            result = safe.getvalue()
            safe.close()
            return result

    @classmethod
    def isSafe(cls, c):
        return c > 47 and c < 58 or c > 64 and c < 91 or c > 96 and c < 123


class ParameterHandlerErrorImpl(ParameterHandlerErrorEvent):
    """Implementation of IErrorEvent interface."""

    def __init__(self, owner, throwable):
        self._owner = owner
        self._throwable = throwable

    def getThrowable(self):
        """Gets the contained throwable.

        @see: L{muntjac.terminal.terminal.IErrorEvent.getThrowable()}
        """
        return self._throwable

    def getParameterHandler(self):
        """Gets the source ParameterHandler.

        @see: L{IErrorEvent.getParameterHandler}
        """
        return self._owner


class URIHandlerErrorImpl(URIHandlerErrorEvent):
    """Implementation of URIHandler.IErrorEvent interface."""

    def __init__(self, owner, throwable):
        self._owner = owner
        self._throwable = throwable

    def getThrowable(self):
        """Gets the contained throwable.

        @see: L{muntjac.terminal.terminal.IErrorEvent.getThrowable()}
        """
        return self._throwable

    def getURIHandler(self):
        """Gets the source URIHandler.

        @see: L{muntjac.terminal.uri_handler.IErrorEvent.getURIHandler}
        """
        return self._owner


class RequestError(TerminalErrorEvent):

    def __init__(self, throwable):
        self._throwable = throwable

    def getThrowable(self):
        return self._throwable
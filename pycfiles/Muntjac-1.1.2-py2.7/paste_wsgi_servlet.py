# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/gwt/server/paste_wsgi_servlet.py
# Compiled at: 2013-04-04 15:36:36
import logging
from urlparse import urlparse
from os.path import join, dirname, normpath
try:
    from cPickle import UnpicklingError
except ImportError:
    from pickle import UnpicklingError

from paste.httpheaders import ACCEPT_LANGUAGE, SCRIPT_NAME, PATH_INFO, IF_MODIFIED_SINCE, USER_AGENT, CONTENT_LENGTH, CONTENT_TYPE
from babel.core import Locale, UnknownLocaleError
import muntjac
from muntjac.util import sys_path_install, defaultLocale
sys_path_install()
from WebKit.HTTPServlet import HTTPServlet
logger = logging.getLogger(__name__)

class EndResponseException(Exception):
    pass


class PasteWsgiServlet(HTTPServlet):
    EndResponse = EndResponseException

    def __init__(self, contextRoot=None, contextPath=None, timeout=1800):
        if contextRoot is not None:
            self.contextRoot = contextRoot
        else:
            root = join(dirname(muntjac.__file__), 'public')
            self.contextRoot = normpath(root)
        self.contextPath = contextPath if contextPath is not None else ''
        self._timeout = timeout
        return

    def awake(self, transaction):
        self.init()

    def respond(self, transaction):
        self.service(transaction.request(), transaction.response())

    def init(self):
        raise NotImplementedError

    def service(self, request, response):
        raise NotImplementedError

    def getContextPath(self, request):
        return self.contextPath

    def originalContextPath(self, request):
        return self.getContextPath(request)

    def getServletPath(self, request):
        servletPath = SCRIPT_NAME(request.environ())
        return servletPath

    def getUrlPath(self, url):
        """
        @param url: URL of the form scheme://netloc/path;parameters?query#frag
        @return: the path part or the url
        """
        return urlparse(url)[2]

    def getResourceAsStream(self, path):
        path = join(self.contextRoot, path.lstrip('/'))
        stream = open(normpath(path), 'rb')
        return stream

    def getResource(self, filename):
        path = join(self.contextRoot, filename.lstrip('/'))
        return path

    def getResourcePath(self, session, path):
        return join(self.contextRoot, path.lstrip('/'))

    def getParameters(self, request):
        return request.fields()

    def getParameter(self, request, key, default=''):
        return request.field(key, default)

    def setParameter(self, request, key, value):
        request.setField(key, value)

    def getHeader(self, request, field):
        return request.serverDictionary().get(field)

    def getUserAgent(self, request):
        return USER_AGENT(request.environ())

    def getContentLength(self, request):
        return CONTENT_LENGTH(request.environ())

    def getContentType(self, request):
        return CONTENT_TYPE(request.environ())

    def getIfModifiedSince(self, request):
        dh = IF_MODIFIED_SINCE(request.environ())
        if dh:
            return int(dh)
        return -1

    def getServerPort(self, request):
        portStr = request.environ().get('SERVER_PORT')
        if portStr is not None:
            return int(portStr)
        else:
            return

    def getRequestUri(self, request):
        """The request's URL from the protocol name up to the query string"""
        return urlparse(request.uri())[2]

    def getPathInfo(self, request):
        return PATH_INFO(request.environ())

    def getLocale(self, request):
        tags = ACCEPT_LANGUAGE.parse(request.environ())
        if tags:
            try:
                return Locale.parse(tags[0], sep='-')
            except UnknownLocaleError as e:
                try:
                    return Locale.parse(tags[0])
                except UnknownLocaleError as e:
                    logger.error('Locale parsing error: %s' % e)
                    return defaultLocale()

        else:
            return defaultLocale()

    def getServerName(self, request):
        return request.environ().get('SERVER_NAME', '')

    def isSecure(self, request):
        """Check whether the request is a HTTPS connection."""
        return request.environ().get('HTTPS', '').lower() == 'on'

    def getInputStream(self, request):
        return request.rawInput()

    def setHeader(self, response, name, value):
        response.setHeader(name, value)

    def setStatus(self, response, n, msg=''):
        response.setStatus(n, msg)

    def write(self, response, value):
        response.write(value)

    def redirect(self, response, url):
        response.sendRedirect(url)

    def getOutputStream(self, response):
        return response

    def getSession(self, request, allowSessionCreation=True):
        try:
            if allowSessionCreation:
                return request.session()
            else:
                if request.transaction().hasSession():
                    return request.session()
                return

        except EOFError as e:
            logger.exception('Session retrieval error: %s' % str(e))
            return
        except UnpicklingError as e:
            logger.exception('Session retrieval error: %s' % str(e))
            return
        except ValueError as e:
            logger.exception('Session retrieval error: %s' % str(e))
            return

        return

    def invalidateSession(self, request):
        try:
            request.session().invalidate()
        except Exception as e:
            logger.error('Session invalidation error: %s' % e)

    def getSessionId(self, request):
        try:
            return request.sessionId()
        except Exception as e:
            logger.error('Session ID error: %s' % e)
            return

        return

    def getSessionAttribute(self, session, name, default=None):
        if session is not None:
            return session.value(name, default)
        else:
            return default
            return

    def setSessionAttribute(self, session, name, value):
        if session is not None:
            session.setValue(name, value)
        return

    def getMaxInactiveInterval(self, session):
        if session is not None:
            return session.value('timeout', self._timeout)
        else:
            return self._timeout
            return

    def isSessionNew(self, session):
        if session is not None:
            return session.isNew()
        else:
            return True
            return
# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pycoon\environment.py
# Compiled at: 2007-03-03 11:04:15
__author__ = 'Andrey Nordin <http://claimid.com/anrienord>'
import os, logging
from urlparse import urlparse
from pycoon.source import SourceResolver

class Environment:
    __module__ = __name__
    prefix = ''
    contentType = None

    def __init__(self, req, isExternal=True, environ=None):
        self.log = logging.getLogger('environment')
        self.prefix = '/'
        self.request = req
        self.response = HttpResponse()
        self.sourceResolver = SourceResolver(self)
        self.componentManager = None
        self.isExternal = isExternal
        self.environ = environ
        self.objectModel = {}
        self.objectModel['request'] = self.request
        self.objectModel['response'] = self.response
        self.objectModel['processor'] = None
        self.objectModel['root-processor'] = None
        self.objectModel['source-resolver'] = self.sourceResolver
        self.log.debug('Created: %s, self.isExternal: %s' % (self, self.isExternal))
        return

    def changeContext(self, newPrefix, contextPath):
        if newPrefix:
            newPrefix = '%s/' % newPrefix
            self.prefix += newPrefix
            splitted = self.request.uri.split(newPrefix, 1)
            if len(splitted) == 2:
                self.request.uri = splitted[1]
            else:
                self.request.uri = ''
        if contextPath:
            if contextPath.find(':') != -1:
                s = contextPath
            else:
                s = '%s/%s' % (self.contextPath, contextPath)
            s = os.path.dirname(s)
            self.contextPath = s
        self.log.debug('New context path: "%s", prefix: "%s"' % (self.contextPath, self.prefix))
        self.log.debug('Request URI: "%s"' % self.request.uri)

    def setContext(self, prefix, uri, contextPath):
        self.prefix = prefix
        self.request.uri = uri
        self.contextPath = contextPath

    def createWrapper(self, uri):
        params = self.request.params.copy()
        (scheme, netloc, path, paramstr, query, fragment) = urlparse(uri)
        if len(query) > 0:
            params.update(dict([ p.split('=') for p in query.split('&') ]))
        req = HttpRequest(path, params, request=self.request)
        env = Environment(req, False)
        env.contextPath = self.contextPath
        env.componentManager = self.componentManager
        env.objectModel['processor'] = self.objectModel['processor']
        env.objectModel['root-processor'] = self.objectModel['root-processor']
        return env


class HttpRequest:
    __module__ = __name__

    def __init__(self, uri, params={}, **kwargs):
        self.params = params
        self.uri = uri
        if 'request' in kwargs:
            req = kwargs.get('request')
            self.formEncoding = req.formEncoding
            self.method = req.method
        else:
            self.formEncoding = None
            self.method = None
        return


class HttpResponse:
    __module__ = __name__
    status = 200
    body = None
    exceptionAware = False

    def __init__(self):
        self.headers = []
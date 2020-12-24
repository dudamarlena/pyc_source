# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pycoon\source.py
# Compiled at: 2007-03-03 11:10:33
__author__ = 'Andrey Nordin <http://claimid.com/anrienord>'
import os, urlparse, urllib2, logging, pkg_resources
from pycoon import ResourceNotFoundException

class Source:
    """
    Encapsulates source access by URI, no matter what URI type is.
    """
    __module__ = __name__
    uri = None

    def getLastModified(self):
        raise NotImplementedError()

    def read(self):
        raise NotImplementedError()

    def exists(self):
        raise NotImplementedError()


class FileSource(Source):
    __module__ = __name__

    def __init__(self, filename, uri=None):
        if uri:
            self.uri = uri
        else:
            self.uri = filename
        self.filename = filename
        logging.getLogger('source.file').debug('Created with filename %s' % filename)

    def getLastModified(self):
        self._checkExist()
        return os.path.getmtime(self.filename)

    def read(self):
        self._checkExist()
        fd = open(self.filename, 'rb')
        try:
            return fd.read()
        finally:
            fd.close()

    def exists(self):
        return os.path.isfile(self.filename)

    def _checkExist(self):
        if not self.exists():
            raise ResourceNotFoundException('File %s not found' % self.filename)


class HttpSource(Source):
    """
    Simple HTTP source that supports only GET requests, thus it is inappropriate
    for REST applications that need the complete set of CRUD actions.
    """
    __module__ = __name__

    def __init__(self, uri):
        self.uri = uri
        logging.getLogger('source.http').debug('Created with URI %s' % self.uri)

    def read(self):
        encoding = os.getenv('file.property')
        if encoding is not None:
            uri = self.uri.encode(encoding)
        else:
            uri = self.uri
        try:
            request = urllib2.Request(uri)
            opener = urllib2.build_opener()
            fd = opener.open(request)
            try:
                return fd.read()
            finally:
                fd.close()
        except urllib2.HTTPError, e:
            raise ResourceNotFoundException('URI not found: %s' % self.uri)

        return


class SitemapSource(Source):
    """
    Represents sitemap pipeline output accessible via cocoon: URI.
    """
    __module__ = __name__

    def __init__(self, uri, env):
        self.log = logging.getLogger('source.sitemap')
        self.uri = 'cocoon:%s' % uri
        self.log.debug('Initializing source with URI: %s' % self.uri)
        if uri.startswith('//'):
            self.processor = env.objectModel['root-processor']
            uri = uri[2:]
            self.env = env.createWrapper(uri)
            self.env.contextPath = self.processor.contextPath
        elif uri.startswith('/'):
            self.processor = env.objectModel['processor']
            uri = uri[1:]
            self.env = env.createWrapper(uri)
        else:
            raise Exception('Malformed cocoon URI: %s' % self.uri)
        self.processingPipeline = self.processor.buildPipeline(self.env)

    def read(self):
        try:
            self.processingPipeline.process(self.env)
        except Exception, e:
            if hasattr(self.processingPipeline, 'handleErrorsNode'):
                self.log.debug('Exception occured, found <map:handle-errros>, handling')
                self.processingPipeline.handleErrorsNode.invoke(self.env, None, e)
            else:
                self.log.debug('Exception occured, no <map:handle-errros>, re-raising')
                raise

        return self.env.response.body


class SourceResolver:
    """
    Allows to get a Source instance for any type of URI.
    """
    __module__ = __name__

    def __init__(self, env=None):
        self.env = env
        self.log = logging.getLogger('source.resolver')

    def resolveUri(self, uri, baseUri=None, params={}):
        if baseUri is None:
            baseUri = self.env.contextPath
        self.log.debug('Resolving URI "%s" with base "%s"' % (uri, baseUri))
        if not uri:
            return
        if not urlparse.urlparse(uri)[0] and baseUri != '':
            uri = '%s/%s' % (baseUri, uri)
        (scheme, netloc, path, params, query, fragment) = urlparse.urlparse(uri)
        if scheme == 'file' or scheme == '':
            if len(path) > 2 and path[2] == ':':
                path = path[1:]
            return FileSource(path, uri)
        elif scheme == 'http':
            return HttpSource(uri)
        elif scheme == 'cocoon':
            return SitemapSource(path, self.env)
        elif scheme == 'rawegg':
            (egg, filename) = path.split(':', 1)
            return FileSource(pkg_resources.resource_filename(egg, filename[1:]), uri)
        else:
            raise Exception('Unknown URI scheme: %s for URI %s' % (scheme, uri))
        return
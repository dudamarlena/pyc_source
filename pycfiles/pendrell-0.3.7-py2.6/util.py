# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pendrell/util.py
# Compiled at: 2010-09-03 02:22:19
import os
from base64 import b64encode
from twisted.python import urlpath
CRLF = '\r\n'

class URLPath(urlpath.URLPath):
    DEFAULT_PORTS = dict(http=80, https=443, ftp=21, file=None)

    def __init__(self, scheme=None, netloc=None, path=None, query=None, fragment=None):
        self.netloc = netloc
        if netloc:
            self.scheme = scheme or 'http'
            try:
                (host, port) = netloc.rsplit(':', 1)
            except ValueError:
                self.host = self.netloc
                self.port = self.DEFAULT_PORTS.get(scheme)
            else:
                self.host = host
                self.port = int(port)
        else:
            self.scheme = scheme or 'file'
            self.host = None
            self.port = None
        assert filter(None, [ hasattr(self, a) for a in ('scheme', 'host', 'port') ])
        assert self.scheme is not None
        self.path = path or '/'
        self.query = query or ''
        self.fragment = fragment or ''
        return

    @classmethod
    def fromRequest(klass, request):
        """Constructor based on Request instance."""
        return klass.fromString(str(request.url))

    def __eq__(self, other):
        return str(self) == str(other)

    def click(self, url):
        newUrl = urlpath.URLPath.click(self, url)
        isDir = newUrl.path.endswith('/')
        path = os.path.normpath(newUrl.path)
        if len(path) == 0 or isDir and not path.endswith('/'):
            path += '/'
        newUrl.path = path
        return newUrl


def humanizeBytes(size):
    suffices = [
     'B', 'KB', 'MB', 'GB', 'TB']
    suffix = suffices.pop(0)
    while size > 1024 and suffices:
        size = float(size / 1024)
        suffix = suffices.pop(0)

    return (size, suffix)


def normalizeBytes(size, suffix):
    suffixOrder = [
     'B', 'KB', 'MB', 'GB', 'TB']
    order = suffixOrder.index(suffix)
    size = long(size * 1024 ** order)
    return size


def b64random(length):
    return b64encode(os.urandom(length))[:length]
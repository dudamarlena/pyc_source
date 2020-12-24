# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/poster/streaminghttp.py
# Compiled at: 2011-04-16 09:24:30
__doc__ = 'Streaming HTTP uploads module.\n\nThis module extends the standard httplib and urllib2 objects so that\niterable objects can be used in the body of HTTP requests.\n\nIn most cases all one should have to do is call :func:`register_openers()`\nto register the new streaming http handlers which will take priority over\nthe default handlers, and then you can use iterable objects in the body\nof HTTP requests.\n\n**N.B.** You must specify a Content-Length header if using an iterable object\nsince there is no way to determine in advance the total size that will be\nyielded, and there is no way to reset an interator.\n\nExample usage:\n\n>>> from StringIO import StringIO\n>>> import urllib2, poster.streaminghttp\n\n>>> opener = poster.streaminghttp.register_openers()\n\n>>> s = "Test file data"\n>>> f = StringIO(s)\n\n>>> req = urllib2.Request("http://localhost:5000", f,\n...                       {\'Content-Length\': str(len(s))})\n'
import httplib, urllib2, socket
from httplib import NotConnected
__all__ = [
 'StreamingHTTPConnection', 'StreamingHTTPRedirectHandler', 'StreamingHTTPHandler', 'register_openers']
if hasattr(httplib, 'HTTPS'):
    __all__.extend(['StreamingHTTPSHandler', 'StreamingHTTPSConnection'])

class _StreamingHTTPMixin:
    """Mixin class for HTTP and HTTPS connections that implements a streaming
    send method."""
    __module__ = __name__

    def send(self, value):
        """Send ``value`` to the server.

        ``value`` can be a string object, a file-like object that supports
        a .read() method, or an iterable object that supports a .next()
        method.
        """
        if self.sock is None:
            if self.auto_open:
                self.connect()
            else:
                raise NotConnected()
        if self.debuglevel > 0:
            print 'send:', repr(value)
        try:
            blocksize = 8192
            if hasattr(value, 'read'):
                if hasattr(value, 'seek'):
                    value.seek(0)
                if self.debuglevel > 0:
                    print 'sendIng a read()able'
                data = value.read(blocksize)
                while data:
                    self.sock.sendall(data)
                    data = value.read(blocksize)

            elif hasattr(value, 'next'):
                if hasattr(value, 'reset'):
                    value.reset()
                if self.debuglevel > 0:
                    print 'sendIng an iterable'
                for data in value:
                    self.sock.sendall(data)

            else:
                self.sock.sendall(value)
        except socket.error, v:
            if v[0] == 32:
                self.close()
            raise

        return


class StreamingHTTPConnection(_StreamingHTTPMixin, httplib.HTTPConnection):
    """Subclass of `httplib.HTTPConnection` that overrides the `send()` method
    to support iterable body objects"""
    __module__ = __name__


class StreamingHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
    """Subclass of `urllib2.HTTPRedirectHandler` that overrides the
    `redirect_request` method to properly handle redirected POST requests

    This class is required because python 2.5's HTTPRedirectHandler does
    not remove the Content-Type or Content-Length headers when requesting
    the new resource, but the body of the original request is not preserved.
    """
    __module__ = __name__
    handler_order = urllib2.HTTPRedirectHandler.handler_order - 1

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        """Return a Request or None in response to a redirect.

        This is called by the http_error_30x methods when a
        redirection response is received.  If a redirection should
        take place, return a new Request to allow http_error_30x to
        perform the redirect.  Otherwise, raise HTTPError if no-one
        else should try to handle this url.  Return None if you can't
        but another Handler might.
        """
        m = req.get_method()
        if code in (301, 302, 303, 307) and m in ('GET', 'HEAD') or code in (301, 302,
                                                                             303) and m == 'POST':
            newurl = newurl.replace(' ', '%20')
            newheaders = dict(((k, v) for (k, v) in req.headers.items() if k.lower() not in ('content-length',
                                                                                             'content-type')))
            return urllib2.Request(newurl, headers=newheaders, origin_req_host=req.get_origin_req_host(), unverifiable=True)
        else:
            raise urllib2.HTTPError(req.get_full_url(), code, msg, headers, fp)


class StreamingHTTPHandler(urllib2.HTTPHandler):
    """Subclass of `urllib2.HTTPHandler` that uses
    StreamingHTTPConnection as its http connection class."""
    __module__ = __name__
    handler_order = urllib2.HTTPHandler.handler_order - 1

    def http_open(self, req):
        """Open a StreamingHTTPConnection for the given request"""
        return self.do_open(StreamingHTTPConnection, req)

    def http_request(self, req):
        """Handle a HTTP request.  Make sure that Content-Length is specified
        if we're using an interable value"""
        if req.has_data():
            data = req.get_data()
            if hasattr(data, 'read') or hasattr(data, 'next'):
                if not req.has_header('Content-length'):
                    raise ValueError('No Content-Length specified for iterable body')
        return urllib2.HTTPHandler.do_request_(self, req)


if hasattr(httplib, 'HTTPS'):

    class StreamingHTTPSConnection(_StreamingHTTPMixin, httplib.HTTPSConnection):
        """Subclass of `httplib.HTTSConnection` that overrides the `send()`
        method to support iterable body objects"""
        __module__ = __name__


    class StreamingHTTPSHandler(urllib2.HTTPSHandler):
        """Subclass of `urllib2.HTTPSHandler` that uses
        StreamingHTTPSConnection as its http connection class."""
        __module__ = __name__
        handler_order = urllib2.HTTPSHandler.handler_order - 1

        def https_open(self, req):
            return self.do_open(StreamingHTTPSConnection, req)

        def https_request(self, req):
            if req.has_data():
                data = req.get_data()
                if hasattr(data, 'read') or hasattr(data, 'next'):
                    if not req.has_header('Content-length'):
                        raise ValueError('No Content-Length specified for iterable body')
            return urllib2.HTTPSHandler.do_request_(self, req)


def get_handlers():
    handlers = [
     StreamingHTTPHandler, StreamingHTTPRedirectHandler]
    if hasattr(httplib, 'HTTPS'):
        handlers.append(StreamingHTTPSHandler)
    return handlers


def register_openers():
    """Register the streaming http handlers in the global urllib2 default
    opener object.

    Returns the created OpenerDirector object."""
    opener = urllib2.build_opener(*get_handlers())
    urllib2.install_opener(opener)
    return opener
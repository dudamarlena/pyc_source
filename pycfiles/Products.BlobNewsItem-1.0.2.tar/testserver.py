# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/Paste-1.7.5.1-py2.6.egg/paste/debug/testserver.py
# Compiled at: 2012-02-27 07:41:58
"""
WSGI Test Server

This builds upon paste.util.baseserver to customize it for regressions
where using raw_interactive won't do.

"""
import time
from paste.httpserver import *

class WSGIRegressionServer(WSGIServer):
    """
    A threaded WSGIServer for use in regression testing.  To use this
    module, call serve(application, regression=True), and then call
    server.accept() to let it handle one request.  When finished, use
    server.stop() to shutdown the server. Note that all pending requests
    are processed before the server shuts down.
    """
    defaulttimeout = 10

    def __init__(self, *args, **kwargs):
        WSGIServer.__init__(self, *args, **kwargs)
        self.stopping = []
        self.pending = []
        self.timeout = self.defaulttimeout
        self.socket.settimeout(2)

    def serve_forever(self):
        from threading import Thread
        thread = Thread(target=self.serve_pending)
        thread.start()

    def reset_expires(self):
        if self.timeout:
            self.expires = time.time() + self.timeout

    def close_request(self, *args, **kwargs):
        WSGIServer.close_request(self, *args, **kwargs)
        self.pending.pop()
        self.reset_expires()

    def serve_pending(self):
        self.reset_expires()
        while not self.stopping or self.pending:
            now = time.time()
            if now > self.expires and self.timeout:
                print '\nWARNING: WSGIRegressionServer timeout exceeded\n'
                break
            if self.pending:
                self.handle_request()
            time.sleep(0.1)

    def stop(self):
        """ stop the server (called from tester's thread) """
        self.stopping.append(True)

    def accept(self, count=1):
        """ accept another request (called from tester's thread) """
        assert not self.stopping
        [ self.pending.append(True) for x in range(count) ]


def serve(application, host=None, port=None, handler=None):
    server = WSGIRegressionServer(application, host, port, handler)
    print 'serving on %s:%s' % server.server_address
    server.serve_forever()
    return server


if __name__ == '__main__':
    import urllib
    from paste.wsgilib import dump_environ
    server = serve(dump_environ)
    baseuri = 'http://%s:%s' % server.server_address

    def fetch(path):
        server.accept(1)
        import socket
        socket.setdefaulttimeout(5)
        return urllib.urlopen(baseuri + path).read()


    assert 'PATH_INFO: /foo' in fetch('/foo')
    assert 'PATH_INFO: /womble' in fetch('/womble')
    server.accept(1)
    server.stop()
    urllib.urlopen(baseuri)
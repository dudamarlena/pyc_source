# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/Paste-1.7.5.1-py2.6.egg/paste/debug/debugapp.py
# Compiled at: 2012-02-27 07:41:58
__doc__ = '\nVarious Applications for Debugging/Testing Purposes\n'
import time
__all__ = [
 'SimpleApplication', 'SlowConsumer']

class SimpleApplication(object):
    """
    Produces a simple web page
    """

    def __call__(self, environ, start_response):
        body = '<html><body>simple</body></html>'
        start_response('200 OK', [('Content-Type', 'text/html'),
         (
          'Content-Length', str(len(body)))])
        return [
         body]


class SlowConsumer(object):
    """
    Consumes an upload slowly...

    NOTE: This should use the iterator form of ``wsgi.input``,
          but it isn't implemented in paste.httpserver.
    """

    def __init__(self, chunk_size=4096, delay=1, progress=True):
        self.chunk_size = chunk_size
        self.delay = delay
        self.progress = True

    def __call__(self, environ, start_response):
        size = 0
        total = environ.get('CONTENT_LENGTH')
        if total:
            remaining = int(total)
            while remaining > 0:
                if self.progress:
                    print '%s of %s remaining' % (remaining, total)
                if remaining > 4096:
                    chunk = environ['wsgi.input'].read(4096)
                else:
                    chunk = environ['wsgi.input'].read(remaining)
                if not chunk:
                    break
                size += len(chunk)
                remaining -= len(chunk)
                if self.delay:
                    time.sleep(self.delay)

            body = '<html><body>%d bytes</body></html>' % size
        else:
            body = '<html><body>\n<form method="post" enctype="multipart/form-data">\n<input type="file" name="file">\n<input type="submit" >\n</form></body></html>\n'
        print 'bingles'
        start_response('200 OK', [('Content-Type', 'text/html'),
         (
          'Content-Length', len(body))])
        return [
         body]


def make_test_app(global_conf):
    return SimpleApplication()


make_test_app.__doc__ = SimpleApplication.__doc__

def make_slow_app(global_conf, chunk_size=4096, delay=1, progress=True):
    from paste.deploy.converters import asbool
    return SlowConsumer(chunk_size=int(chunk_size), delay=int(delay), progress=asbool(progress))


make_slow_app.__doc__ = SlowConsumer.__doc__
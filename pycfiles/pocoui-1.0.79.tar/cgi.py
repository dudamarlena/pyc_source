# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/wrappers/cgi.py
# Compiled at: 2006-12-26 17:18:07
__doc__ = '\n    pocoo.wrappers.cgi\n    ~~~~~~~~~~~~~~~~~~\n\n    Pocoo CGI wrapper, mostly copied from PEP 333.\n\n    Usage::\n\n        from pocoo.wrappers.cgi import run_cgi\n        run_cgi("/path/to/instance/root")\n\n    For more information, see `pocoo.wrappers`.\n\n\n    :copyright: 2003 by Phillip J. Eby.\n    :copyright: 2006 by Georg Brandl.\n    :license: GNU GPL, see LICENSE for more details.\n'
import os, sys

def run_cgi(instancedir, stream=sys.stdout):
    """
    Run a Pocoo instance as a CGI script.

    :param instancedir: the instance root directory
    :type instancedir: string

    :param stream: the stream to write the output to. Normally
        this is ``sys.stdout``.
    """
    from pocoo.context import ApplicationContext
    ctx = ApplicationContext(instancedir, is_cgi=True)
    environ = dict(os.environ.items())
    environ['wsgi.input'] = sys.stdin
    environ['wsgi.errors'] = sys.stderr
    environ['wsgi.version'] = (1, 0)
    environ['wsgi.multithread'] = False
    environ['wsgi.multiprocess'] = True
    environ['wsgi.run_once'] = True
    if environ.get('HTTPS', 'off') in ('on', '1'):
        environ['wsgi.url_scheme'] = 'https'
    else:
        environ['wsgi.url_scheme'] = 'http'
    headers_set = []
    headers_sent = []

    def write(data):
        if not headers_set:
            raise AssertionError('write() before start_response()')
        elif not headers_sent:
            (status, response_headers) = headers_sent[:] = headers_set
            stream.write('Status: %s\r\n' % status)
            for header in response_headers:
                stream.write('%s: %s\r\n' % header)

            stream.write('\r\n')
        stream.write(data)
        stream.flush()

    def start_response(status, response_headers, exc_info=None):
        if exc_info:
            try:
                if headers_sent:
                    raise exc_info[0], exc_info[1], exc_info[2]
            finally:
                exc_info = None
        elif headers_set:
            raise AssertionError('Headers already set!')
        headers_set[:] = [status, response_headers]
        return write

    result = ctx(environ, start_response)
    try:
        for data in result:
            if data:
                write(data)

        if not headers_sent:
            write('')
    finally:
        if hasattr(result, 'close'):
            result.close()
    return


def run_profiled_cgi(instancedir, stream=None):
    """
    Run the Pocoo instance in ``instancedir``, collect profiling
    information and write that back to the web server.

    :param instancedir: The instance root directory.
    :param stream: Stream to write real HTML output to.
        If it is ``None``, write to a ``StringIO`` buffer.
    """
    import pstats, cStringIO
    try:
        import cProfile as profile
    except ImportError:
        import profile

    if stream is None:
        stream = cStringIO.StringIO()
    sys.stdout.write('Content-Type: text/plain\r\n\r\n')
    glob = globals()
    glob['stream'] = stream
    glob['instancedir'] = instancedir
    profile.runctx('run_cgi(instancedir, stream)', glob, None, '/tmp/profile.data')
    stat = pstats.Stats('/tmp/profile.data')
    stat.sort_stats('cumulative')
    stat.print_stats()
    return


if __name__ == '__main__':
    run_cgi(sys.argv[1])
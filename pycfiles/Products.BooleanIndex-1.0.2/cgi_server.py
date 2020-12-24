# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/PasteScript-1.7.5-py2.6.egg/paste/script/cgi_server.py
# Compiled at: 2012-02-27 07:41:53
import os, sys

def paste_run_cgi(wsgi_app, global_conf):
    run_with_cgi(wsgi_app)


stdout = sys.__stdout__

def run_with_cgi(application):
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
            stdout.write('Status: %s\r\n' % status)
            for header in response_headers:
                stdout.write('%s: %s\r\n' % header)

            stdout.write('\r\n')
        stdout.write(data)
        stdout.flush()

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

    result = application(environ, start_response)
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
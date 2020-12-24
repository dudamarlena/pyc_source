# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_server.py
# Compiled at: 2010-10-23 10:59:01
import webob

def app(environ, start_response):
    request = webob.Request(environ)
    if request.path == '/redirect':
        start_response('301 MOVED', [('Location', '/foo')])
        return '301 MOVED'
    elif request.path == '/needs_auth':
        auth = request.headers.get('Authorization')
        if auth and auth.startswith('Basic'):
            (user, passwd) = auth.split()[(-1)].decode('base64').split(':')
        else:
            user = None
        if user != 'john':
            start_response('401 Unauthorized', [('WWW-Authenticate', 'Basic realm="default"')])
            return '401 Unauthorized'
    start_response('200 OK', [('Content-Type', 'text/plain')])
    retval = ['Path: %s' % request.path]
    keys = request.params.keys()
    keys.sort()
    for k in keys:
        v = request.params[k]
        if hasattr(v, 'file'):
            v = v.file.read()
        retval.append('%s: %s' % (k, v))

    return ('\n').join(retval)


if __name__ == '__main__':
    import sys
    from paste.httpserver import serve
    port = int(sys.argv[1])
    if len(sys.argv) == 3 and sys.argv[2] == 'ssl':
        ssl_pem = '*'
    else:
        ssl_pem = None
    try:
        serve(app, 'localhost', port, ssl_pem=ssl_pem)
    except KeyboardInterrupt:
        pass
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/substrate/data/local/substrate/lib/webtest/debugapp.py
# Compiled at: 2012-02-03 19:38:43
from webob import Request, Response
from webtest.compat import to_bytes
__all__ = ['debug_app']

def debug_app(environ, start_response):
    req = Request(environ)
    if req.path_info == '/form.html' and req.method == 'GET':
        resp = Response(content_type='text/html')
        resp.body = to_bytes('<html><body>\n        <form action="/form-submit" method="POST">\n            <input type="text" name="name">\n            <input type="submit" name="submit" value="Submit!">\n        </form></body></html>')
        return resp(environ, start_response)
    if 'error' in req.GET:
        raise Exception('Exception requested')
    status = str(req.GET.get('status', '200 OK'))
    parts = []
    for name, value in sorted(environ.items()):
        if name.upper() != name:
            value = repr(value)
        parts.append('%s: %s\n' % (name, value))

    if req.content_length:
        req_body = req.body
    else:
        req_body = ''
    if req_body:
        parts.append(to_bytes('-- Body ----------\n'))
        parts.append(req_body)
    body = to_bytes('').join([ to_bytes(p) for p in parts ])
    if status[:3] in ('204', '304') and not req_body:
        body = to_bytes('')
    headers = [
     ('Content-Type', 'text/plain'),
     (
      'Content-Length', str(len(body)))]
    for name, value in req.GET.items():
        if name.startswith('header-'):
            header_name = name[len('header-'):]
            headers.append((header_name, value))

    start_response(str(status), headers)
    if req.method == 'HEAD':
        return [to_bytes('')]
    return [
     body]


def make_debug_app(global_conf):
    """
    An application that displays the request environment, and does
    nothing else (useful for debugging and test purposes).
    """
    return debug_app
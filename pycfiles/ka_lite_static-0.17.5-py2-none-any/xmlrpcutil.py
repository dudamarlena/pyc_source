# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/cherrypy/cherrypy/lib/xmlrpcutil.py
# Compiled at: 2018-07-11 18:15:31
import sys, cherrypy
from cherrypy._cpcompat import ntob

def get_xmlrpclib():
    try:
        import xmlrpc.client as x
    except ImportError:
        import xmlrpclib as x

    return x


def process_body():
    """Return (params, method) from request body."""
    try:
        return get_xmlrpclib().loads(cherrypy.request.body.read())
    except Exception:
        return (('ERROR PARAMS',), 'ERRORMETHOD')


def patched_path(path):
    """Return 'path', doctored for RPC."""
    if not path.endswith('/'):
        path += '/'
    if path.startswith('/RPC2/'):
        path = path[5:]
    return path


def _set_response(body):
    response = cherrypy.response
    response.status = '200 OK'
    response.body = ntob(body, 'utf-8')
    response.headers['Content-Type'] = 'text/xml'
    response.headers['Content-Length'] = len(body)


def respond(body, encoding='utf-8', allow_none=0):
    xmlrpclib = get_xmlrpclib()
    if not isinstance(body, xmlrpclib.Fault):
        body = (
         body,)
    _set_response(xmlrpclib.dumps(body, methodresponse=1, encoding=encoding, allow_none=allow_none))


def on_error(*args, **kwargs):
    body = str(sys.exc_info()[1])
    xmlrpclib = get_xmlrpclib()
    _set_response(xmlrpclib.dumps(xmlrpclib.Fault(1, body)))
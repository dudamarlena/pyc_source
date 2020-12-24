# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/http.py
# Compiled at: 2017-07-27 15:27:56
from __future__ import unicode_literals
from __future__ import print_function
from .enum import Enum
from .html import escape
from . import __version__
from .compat import text_type

class StatusCode(Enum):

    def __repr__(self):
        return b'<httpstatus %s (%s)>' % (int(self), text_type(self))

    _continue = 100
    switching_protocols = 101
    ok = 200
    created = 201
    accepted = 202
    non_authorative_information = 203
    no_content = 204
    reset_content = 205
    partial_content = 206
    multiple_choices = 300
    moved_permanently = 301
    found = 302
    see_other = 303
    not_modified = 304
    use_proxy = 305
    temporary_redirect = 307
    permanent_redirect = 308
    bad_request = 400
    unauthorized = 401
    payment_required = 402
    forbidden = 403
    not_found = 404
    method_not_allowed = 405
    not_acceptable = 406
    proxy_authentication_requred = 407
    request_timeout = 408
    conflict = 409
    gone = 410
    length_required = 411
    precondition_failed = 412
    request_entity_too_large = 413
    request_uri_too_long = 414
    unsupported_media_type = 415
    request_range_not_satisfiable = 416
    expectation_failed = 417
    im_a_teapot = 418
    internal_error = 500
    no_implemented = 501
    bad_gateway = 502
    service_unavailable = 503
    gateway_timeout = 504
    http_version_not_supported = 505


class RespondWith(object):
    status = StatusCode.ok

    def __init__(self, status=None, headers=None):
        if status is not None:
            self.status = status
        self.headers = headers
        return

    def __unicode__(self):
        return get_status_description(self.status)

    def __repr__(self):
        return (b'<respondwith {} "{}">').format(self.status, get_status_description(self.status))


class RespondNotFound(RespondWith):
    status = StatusCode.not_found


class RespondForbidden(RespondWith):
    status = StatusCode.forbidden


class RespondUnauthorized(RespondWith):
    status = StatusCode.unauthorized


def get_status_description(status):
    status = StatusCode(status)
    if not status.is_valid():
        return b'unknown'
    desc = text_type(status).replace(b'_', b' ').title()
    return desc


_error_msgs = {StatusCode.not_found: b'Not Found', 
   StatusCode.internal_error: b'Internal Error'}
_standard_html = b'<!DOCTYPE html>\n<html>\n<head>\n    <meta http-equiv="content-type" content="text/html;charset=utf-8">\n    <title>{status} {msg}</title>\n    <style type="text/css">\n        body {{font-family: arial,sans-serif;}}\n    </style>\n</head>\n<body>\n    <h2>{status} {msg}</h2>\n    <pre>Moya was unable to return a response for resource <strong>{path}</strong></pre>\n    <hr/>\n    <small>Moya {version}</small>\n    <small><a href="https://www.moyaproject.com">http://moyaproject.com</a></small>\n</body>\n'
_debug_html = b'<!DOCTYPE html>\n<html>\n<head>\n    <meta http-equiv="content-type" content="text/html;charset=utf-8">\n    <title>{status} {msg}</title>\n    <style type="text/css">\n        body {{font-family: arial,sans-serif;}}\n    </style>\n</head>\n<body>\n    <h2>{status} {msg}</h2>\n    <pre>Moya was unable to return a response for resource <strong>{path}</strong></pre>\n    <p><strong>{error}</strong></p>\n    <p><em>Moya was unable to render "{status}.html" in order to display a more detailed response</em></p>\n\n    <pre>{trace}</pre>\n    <hr/>\n    <small>Moya {version}</small>\n    <small><a href="https://www.moyaproject.com">http://moyaproject.com</a></small>\n</body>\n'

def standard_response(status, path, error, trace, debug=False):
    """Produces a standard response for a resource if it wasn't handled by the project logic"""
    status = StatusCode(status)
    msg = get_status_description(status)
    if debug:
        html = _debug_html
    else:
        html = _standard_html
    return html.format(version=__version__, status=int(status), path=escape(path), msg=escape(msg), error=escape(text_type(error or b'')), trace=escape(text_type(trace or b'')))


if __name__ == b'__main__':
    print(StatusCode.not_found)
    print(StatusCode(b'not_found'))
    print(StatusCode(404))
    print(int(StatusCode(b'not_found')))
    print(StatusCode.choices)
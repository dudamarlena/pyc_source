# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/csrfmiddleware/__init__.py
# Compiled at: 2009-02-20 14:45:02
"""
Cross Site Request Forgery Middleware.

This is a middleware that implements protection against request
forgeries from other sites.

This is a Pylons port of Luke Plant's django version.

"""
from webob import Request
from webob.exc import HTTPForbidden
import re, itertools
_ERROR_MSG = 'Cross Site Request Forgery detected. Request aborted.'
_POST_FORM_RE = re.compile('(<form\\W[^>]*\\bmethod=(\\\'|"|)POST(\\\'|"|)\\b[^>]*>)', re.IGNORECASE)
_HTML_TYPES = ('text/html', 'application/xhtml+xml')

class CsrfMiddleware(object):
    """Middleware that adds protection against Cross Site
    Request Forgeries by adding hidden form fields to POST forms and 
    checking requests for the correct value. It expects beaker to be upstream
    to insert the session into the environ 
    """

    def __init__(self, app, config):
        self.app = app
        self.unprotected_path = config.get('csrf.unprotected_path')

    def __call__(self, environ, start_response):
        request = Request(environ)
        session = environ['beaker.session']
        session.save()
        if request.method == 'POST':
            if self.unprotected_path is not None and request.path_info.startswith(self.unprotected_path):
                resp = request.get_response(self.app)
                return resp(environ, start_response)
            csrf_token = session.id
            try:
                request_csrf_token = request.POST['csrfmiddlewaretoken']
                if request_csrf_token != csrf_token:
                    resp = HTTPForbidden(_ERROR_MSG)
                else:
                    resp = request.get_response(self.app)
            except KeyError:
                resp = HTTPForbidden(_ERROR_MSG)

        else:
            resp = request.get_response(self.app)
        if resp.status_int != 200:
            return resp(environ, start_response)
        session = environ['beaker.session']
        csrf_token = session.id
        if resp.content_type.split(';')[0] in _HTML_TYPES:
            idattributes = itertools.chain(('id="csrfmiddlewaretoken"', ), itertools.repeat(''))

            def add_csrf_field(match):
                """Returns the matched <form> tag plus the added <input> element"""
                return match.group() + '<div style="display:none;">' + '<input type="hidden" ' + idattributes.next() + ' name="csrfmiddlewaretoken" value="' + csrf_token + '" /></div>'

            resp.body = _POST_FORM_RE.sub(add_csrf_field, resp.body)
        return resp(environ, start_response)


def make_csrf_filter(global_conf, **kw):
    """this is suitable for the paste filter entry point"""

    def filter(app):
        return CsrfMiddleware(app, kw)

    return filter


def make_csrf_filter_app(app, global_conf, **kw):
    """this is suitable for the paste filter-app entry point"""
    return CsrfMiddleware(app, kw)
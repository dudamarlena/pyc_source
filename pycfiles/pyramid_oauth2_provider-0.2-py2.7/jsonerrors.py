# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/pyramid_oauth2_provider/jsonerrors.py
# Compiled at: 2013-02-09 19:59:16
"""
Custom HTTP exceptions that support rendering to JSON by default.
"""
from string import Template
from pyramid import httpexceptions
from pyramid.httpexceptions import text_type
from pyramid.httpexceptions import _no_escape
from pyramid.httpexceptions import WSGIHTTPException

def _quote_escape(value):
    v = _no_escape(value)
    return v.replace('"', '\\"')


class BaseJsonHTTPError(WSGIHTTPException):
    """
    Base error class for rendering errors in JSON.
    """
    json_template_obj = Template('{\n    "status": "${status}",\n    "code": ${code},\n    "explanation": "${explanation}",\n    "detail": "${detail}"\n}\n${html_comment}\n')

    def prepare(self, environ):
        """
        Always return errors in JSON.
        """
        if not self.body and not self.empty_body:
            html_comment = ''
            comment = self.comment or ''
            accept = environ.get('HTTP_ACCEPT', '')
            if 'text/plain' in accept:
                self.content_type = 'text/plain'
                escape = _no_escape
                page_template = self.plain_template_obj
                br = '\n'
                if comment:
                    html_comment = escape(comment)
            else:
                self.content_type = 'aplication/json'
                escape = _quote_escape
                page_template = self.json_template_obj
                br = '\n'
                if comment:
                    html_comment = '# %s' % comment
                args = {'br': br, 'explanation': escape(self.explanation), 
                   'detail': escape(self.detail or ''), 
                   'comment': escape(comment), 
                   'html_comment': html_comment}
                for k, v in environ.items():
                    if not k.startswith('wsgi.') and '.' in k:
                        continue
                    args[k] = escape(v)

                for k, v in self.headers.items():
                    args[k.lower()] = escape(v)

            page = page_template.substitute(status=self.status, code=self.code, **args)
            if isinstance(page, text_type):
                page = page.encode(self.charset)
            self.app_iter = [
             page]
            self.body = page


class HTTPBadRequest(httpexceptions.HTTPBadRequest, BaseJsonHTTPError):
    pass


class HTTPUnauthorized(httpexceptions.HTTPUnauthorized, BaseJsonHTTPError):
    pass


class HTTPMethodNotAllowed(httpexceptions.HTTPMethodNotAllowed, BaseJsonHTTPError):
    pass
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/pyramid_oauth2_provider/errors.py
# Compiled at: 2013-02-09 19:59:16
from pyramid.httpexceptions import text_type
from pyramid.httpexceptions import _no_escape
from pyramid.httpexceptions import _html_escape
from pyramid.httpexceptions import WSGIHTTPException

class BaseJsonHTTPError(WSGIHTTPException):
    """
    Base error class for rendering errors in JSON.
    """

    def prepare(self, environ):
        """
        Always return errors in JSON.
        """
        if not self.body and not self.empty_body:
            html_comment = ''
            comment = self.comment or ''
            accept = environ.get('HTTP_ACCEPT', '')
            if accept and 'html' in accept or '*/*' in accept:
                self.content_type = 'text/html'
                escape = _html_escape
                page_template = self.html_template_obj
                br = '<br/>'
                if comment:
                    html_comment = '<!-- %s -->' % escape(comment)
            elif 'text/plain' in accept:
                self.content_type = 'text/plain'
                escape = _no_escape
                page_template = self.plain_template_obj
                br = '\n'
                if comment:
                    html_comment = escape(comment)
            else:
                self.content_type = 'application/json'
                escape = _no_escape
                page_template = ''
            args = {'br': br, 'explanation': escape(self.explanation), 
               'detail': escape(self.detail or ''), 
               'comment': escape(comment), 
               'html_comment': html_comment}
            body_tmpl = self.body_template_obj
            if WSGIHTTPException.body_template_obj is not body_tmpl:
                for k, v in environ.items():
                    if not k.startswith('wsgi.') and '.' in k:
                        continue
                    args[k] = escape(v)

                for k, v in self.headers.items():
                    args[k.lower()] = escape(v)

            body = body_tmpl.substitute(args)
            page = page_template.substitute(status=self.status, body=body)
            if isinstance(page, text_type):
                page = page.encode(self.charset)
            self.app_iter = [
             page]
            self.body = page


class BaseOauth2Error(dict):
    error_name = None

    def __init__(self, **kw):
        dict.__init__(self)
        if kw:
            self.update(kw)
        self['error'] = self.error_name
        if 'error_description' not in self:
            self['error_description'] = self.__doc__


class InvalidRequest(BaseOauth2Error):
    """
    The request is missing a required parameter, includes an unsupported
    parameter or parameter value, repeats the same parameter, uses more
    than one method for including an access token, or is otherwise
    malformed.  The resource server SHOULD respond with the HTTP 400
    (Bad Request) status code.

    http://tools.ietf.org/html/draft-ietf-oauth-v2-bearer-23#section-3.1
    """
    error_name = 'invalid_request'


class InvalidClient(BaseOauth2Error):
    """
    The provided authorization grant is invalid, expired, revoked, or
    was issued to another cilent.

    http://tools.ietf.org/html/draft-ietf-oauth-v2-31#section-5.2
    """
    error_name = 'invalid_client'


class UnauthorizedClient(BaseOauth2Error):
    """
    The authenticated user is not authorized to use this authorization
    grant type.

    http://tools.ietf.org/html/draft-ietf-oauth-v2-31#section-5.2
    """
    error_name = 'unauthorized_client'


class UnsupportedGrantType(BaseOauth2Error):
    """
    The authorizaiton grant type is not supported by the authorization
    server.

    http://tools.ietf.org/html/draft-ietf-oauth-v2-31#section-5.2
    """
    error_name = 'unsupported_grant_type'


class InvalidToken(BaseOauth2Error):
    """
    The access token provided is expired, revoked, malformed, or
    invalid for other reasons.  The resource SHOULD respond with the
    HTTP 401 (Unauthorized) status code.  The client MAY request a new
    access token and retry the protected resource request.

    http://tools.ietf.org/html/draft-ietf-oauth-v2-bearer-23#section-3.1
    """
    error_name = 'invalid_token'
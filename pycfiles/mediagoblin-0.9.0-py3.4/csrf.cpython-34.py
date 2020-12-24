# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/meddleware/csrf.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 5257 bytes
import random, logging
from werkzeug.exceptions import Forbidden
from wtforms import Form, HiddenField, validators
from mediagoblin import mg_globals
from mediagoblin.meddleware import BaseMeddleware
from mediagoblin.tools.translate import lazy_pass_to_ugettext as _
_log = logging.getLogger(__name__)
if hasattr(random, 'SystemRandom'):
    getrandbits = random.SystemRandom().getrandbits
else:
    getrandbits = random.getrandbits

def csrf_exempt(func):
    """Decorate a Controller to exempt it from CSRF protection."""
    func.csrf_enabled = False
    return func


class CsrfForm(Form):
    __doc__ = 'Simple form to handle rendering a CSRF token and confirming it\n    is included in the POST.'
    csrf_token = HiddenField('', [
     validators.InputRequired()])


def render_csrf_form_token(request):
    """Render the CSRF token in a format suitable for inclusion in a
    form."""
    if 'CSRF_TOKEN' not in request.environ:
        return
    form = CsrfForm(csrf_token=request.environ['CSRF_TOKEN'])
    return form.csrf_token


class CsrfMeddleware(BaseMeddleware):
    __doc__ = 'CSRF Protection Meddleware\n\n    Adds a CSRF Cookie to responses and verifies that it is present\n    and matches the form token for non-safe requests.\n    '
    CSRF_KEYLEN = 64
    SAFE_HTTP_METHODS = ('GET', 'HEAD', 'OPTIONS', 'TRACE')

    def process_request(self, request, controller):
        """For non-safe requests, confirm that the tokens are present
        and match.
        """
        try:
            request.environ['CSRF_TOKEN'] = request.cookies[mg_globals.app_config['csrf_cookie_name']]
        except KeyError:
            request.environ['CSRF_TOKEN'] = self._make_token(request)

        if getattr(controller, 'csrf_enabled', True) and request.method not in self.SAFE_HTTP_METHODS and ('gmg.verify_csrf' in request.environ or 'paste.testing' not in request.environ):
            return self.verify_tokens(request)

    def process_response(self, request, response):
        """Add the CSRF cookie to the response if needed and set Vary
        headers.
        """
        response.set_cookie(mg_globals.app_config['csrf_cookie_name'], request.environ['CSRF_TOKEN'], path=request.environ['SCRIPT_NAME'], domain=mg_globals.app_config.get('csrf_cookie_domain'), secure=request.scheme.lower() == 'https', httponly=True)
        response.vary = list(getattr(response, 'vary', None) or []) + ['Cookie']

    def _make_token(self, request):
        """Generate a new token to use for CSRF protection."""
        return '%s' % (getrandbits(self.CSRF_KEYLEN),)

    def verify_tokens(self, request):
        """Verify that the CSRF Cookie exists and that it matches the
        form value."""
        cookie_token = request.cookies.get(mg_globals.app_config['csrf_cookie_name'], None)
        if cookie_token is None:
            _log.error('CSRF cookie not present')
            raise Forbidden(_('CSRF cookie not present. This is most likely the result of a cookie blocker or somesuch. Make sure to permit the setting of cookies for this domain.'))
        form = CsrfForm(request.form)
        if form.validate():
            form_token = form.csrf_token.data
            if form_token == cookie_token:
                return
        errstr = 'CSRF validation failed'
        _log.error(errstr)
        raise Forbidden(errstr)
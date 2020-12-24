# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\identity\visitor.py
# Compiled at: 2011-11-20 06:12:27
"""The visit and identity management *plugins* are defined here."""
__all__ = [
 'IdentityVisitPlugin', 'create_extension_model', 'shutdown_extension', 'start_extension']
import base64, logging
from cherrypy import request
from formencode.variabledecode import variable_decode, variable_encode
from turbogears import config, visit
from turbogears.identity import create_default_provider, set_current_identity, set_current_provider, set_login_attempted
from turbogears.identity.exceptions import IdentityConfigurationException, IdentityException, IdentityFailure
log = logging.getLogger('turbogears.identity')
_plugin = None

def start_extension():
    """Register the IdentityVisitPlugin with the visit plugin framework.

    Also sets up the configured Identity provider.

    """
    global _plugin
    if not config.get('identity.on', False):
        return
    if not config.get('visit.on', False):
        raise IdentityConfigurationException('Visit tracking must be enabled (via visit.on).')
    if _plugin:
        log.info('Identity already started')
        return
    log.info('Identity starting')
    create_extension_model()
    _plugin = IdentityVisitPlugin()
    visit.enable_visit_plugin(_plugin)


def shutdown_extension():
    """Stops the IdentityVisitPlugin."""
    global _plugin
    if not config.get('identity.on', False):
        return
    if not _plugin:
        log.info('Identity already shut down')
        return
    visit.disable_visit_plugin(_plugin)
    _plugin = None
    log.info('Identity has been shut down.')
    return


def create_extension_model():
    """Create the identity provider object."""
    provider = create_default_provider()
    provider.create_provider_model()


class IdentityVisitPlugin(object):
    """Visit plugin tying the Identity framework to the visit management."""
    __module__ = __name__

    def __init__(self):
        log.info('Identity visit plugin initialized')
        get = config.get
        self.provider = create_default_provider()
        self.user_name_field = get('identity.form.user_name', 'user_name')
        self.password_field = get('identity.form.password', 'password')
        self.submit_button_name = get('identity.form.submit', 'login')
        sources = filter(None, map(str.strip, get('identity.source', 'form,http_auth,visit').split(',')))
        if not sources:
            raise IdentityConfigurationException('You must set some identity source (via identity.source).')
        if 'http_auth' in sources and not get('identity.http_basic_auth'):
            sources.remove('http_auth')
        if 'visit' in sources and not get('visit.on'):
            sources.remove('visit')
        if not sources:
            raise IdentityConfigurationException('You must activate at least one of the identity sources.')
        self.identity_sources = list()
        for s in sources:
            if s:
                try:
                    source_method = getattr(self, 'identity_from_' + s)
                except AttributeError:
                    raise IdentityConfigurationException('Invalid identity source: %s (check identity.source)' % s)
                else:
                    self.identity_sources.append(source_method)

        return

    def identity_from_request(self, visit_key):
        """Retrieve identity information from the HTTP request.

        Checks first for form fields defining the identity then for a cookie.
        If no identity is found, returns an anonymous identity.

        """
        identity = None
        log.debug('Retrieving identity for visit: %s', visit_key)
        for source in self.identity_sources:
            identity = source(visit_key)
            if identity:
                return identity

        log.debug('No identity found')
        identity = self.provider.anonymous_identity()
        return identity

    def decode_basic_credentials(self, credentials):
        """Decode base64 user_name:password credentials used in Basic Auth.

        Returns a list with username in element 0 and password in element 1.

        """
        credentials = base64.decodestring(credentials.strip())
        try:
            credentials = credentials.decode('utf-8')
        except UnicodeError:
            try:
                credentials = credentials.decode('latin-1')
            except UnicodeError:
                credentials = ''

        credentials = credentials.split(':', 1)
        if len(credentials) < 2:
            credentials.append('')
        return credentials

    def identity_from_http_auth(self, visit_key):
        """Try to get authentication data from Authorization request header.

        Only HTTP basic auth is handled at the moment.

        """
        try:
            authorisation = request.headers['Authorization']
        except KeyError:
            return

        (authScheme, schemeData) = authorisation.split(' ', 1)
        if authScheme.lower() != 'basic':
            log.error('HTTP Auth is not basic')
            return
        (user_name, password) = self.decode_basic_credentials(schemeData)
        set_login_attempted(True)
        return self.provider.validate_identity(user_name, password, visit_key)

    def identity_from_visit(self, visit_key):
        """Load identity from Identity provider."""
        return self.provider.load_identity(visit_key)

    def identity_from_form(self, visit_key):
        """Inspect the request params to pull out identity information.

        Must have fields for user name, password, and a login submit button.

        Returns an identity object whose class depends on the current identity
        provider or None if the form contained no identity information or the
        information was incorrect.

        """
        params = request.params
        if params.pop(self.submit_button_name, None) is None:
            return
        params.pop(self.submit_button_name + '.x', None)
        params.pop(self.submit_button_name + '.y', None)
        user_name = params.pop(self.user_name_field, None)
        password = params.pop(self.password_field, None)
        if user_name is None:
            log.error('Missing user name in login form')
            return
        elif isinstance(user_name, list):
            log.error('Multiple user names in login form')
            return
        if password is None:
            log.error('Missing password in login form')
            return
        elif isinstance(password, list):
            log.error('Multiple passwords in login form')
            return
        set_login_attempted(True)
        identity = self.provider.validate_identity(user_name, password, visit_key)
        if identity is None:
            log.warning("The credentials specified weren't valid")
            return
        return identity

    def record_request(self, visit):
        """Authenticate request and try to associate the visit with an identity."""
        if not config.get('identity.on', False):
            log.debug('Identity is not enabled. Setting current identity to None')
            set_current_identity(None)
            return
        if 'identity.path_info' in request.wsgi_environ:
            request.path_info = request.wsgi_environ.pop('identity.path_info')
            request.params = request.wsgi_environ.pop('identity.params', {})
        try:
            identity = self.identity_from_request(visit.key)
        except IdentityException, e:
            log.exception('Caught exception while getting identity from request')
            errors = [str(e)]
            raise IdentityFailure(errors)

        log.debug('Identity is available...')
        set_current_identity(identity)
        set_current_provider(self.provider)
        return
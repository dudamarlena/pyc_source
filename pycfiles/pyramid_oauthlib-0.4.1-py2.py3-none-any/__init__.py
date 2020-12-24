# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/pyramid_oauth2_provider/__init__.py
# Compiled at: 2013-03-11 22:09:01
from sqlalchemy import engine_from_config
from pyramid.config import Configurator
from pyramid.exceptions import ConfigurationError
from pyramid.interfaces import IAuthenticationPolicy
from .models import initialize_sql
from .interfaces import IAuthCheck
from .authentication import OauthAuthenticationPolicy
from . import tests

def includeme(config):
    settings = config.registry.settings
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine, settings)
    if not config.registry.queryUtility(IAuthenticationPolicy):
        config.set_authentication_policy(OauthAuthenticationPolicy())
    auth_check = settings.get('oauth2_provider.auth_checker')
    if not auth_check:
        raise ConfigurationError('You must provide an implementation of the authentication check interface that is included with pyramid_oauth2_provider for verifying usernames and passwords')
    policy = config.maybe_dotted(auth_check)
    config.registry.registerUtility(policy, IAuthCheck)
    config.add_route('oauth2_provider_authorize', '/oauth2/authorize')
    config.add_route('oauth2_provider_token', '/oauth2/token')
    config.scan()


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    includeme(config)
    return config.make_wsgi_app()
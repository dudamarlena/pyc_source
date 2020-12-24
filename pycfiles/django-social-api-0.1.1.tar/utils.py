# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-social-api/social_api/utils.py
# Compiled at: 2016-02-27 04:28:12
import time
from django.utils.module_loading import import_string
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.test.utils import override_settings
from .storages.base import TokensStorageAbstractBase
from .exceptions import CallsLimitError

def get_storages_default():
    storages = getattr(settings, 'SOCIAL_API_TOKENS_STORAGES', None)
    if storages is None:
        storages_default = [('social_api.storages.oauthtokens.OAuthTokensStorage', 'oauth_tokens'),
         ('social_api.storages.social_auth.SocialAuthTokensStorage', 'social.apps.django_app.default')]
        storages = [ storage for storage, app in storages_default if app in settings.INSTALLED_APPS ]
        if not storages:
            raise ImproperlyConfigured('No available token storages found for social_api application. Add to INSTALLES_APPS at least one storage: social_auth or oauth_tokens or provide custom setting SOCIAL_API_TOKENS_STORAGES')
    return storages


STORAGES = get_storages_default()

def get_storages(*args, **kwargs):
    for import_path in STORAGES:
        yield get_storage(import_path, *args, **kwargs)


def get_storage(import_path, *args, **kwargs):
    """
    Imports the staticfiles finder class described by import_path, where
    import_path is the full Python path to the class.
    """
    TokensStorage = import_string(import_path)
    if not issubclass(TokensStorage, TokensStorageAbstractBase):
        raise ImproperlyConfigured('TokensStorage "%s" is not a subclass of "%s"' % TokensStorageAbstractBase)
    return TokensStorage(*args, **kwargs)


def override_api_context(provider, **kwargs):
    context = getattr(settings, 'SOCIAL_API_CALL_CONTEXT', {provider: {}}).get(provider, {})
    context.update(kwargs)
    return override_settings(SOCIAL_API_CALL_CONTEXT={provider: context})


def limit_errored_calls(error, limit):

    def _inner_decorator(fn):
        fn.count = 1

        def _inner_function(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except error:
                if fn.count < limit:
                    time.sleep(1)
                    fn.count += 1
                    return _inner_function(*args, **kwargs)
                raise CallsLimitError('Limit of calls %s method %s achieved' % (limit, fn))

        return _inner_function

    return _inner_decorator
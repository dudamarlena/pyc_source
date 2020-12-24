# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/jeremydw/git/edu-buy-flow/lib/airlock/config.py
# Compiled at: 2015-03-23 12:28:51
__doc__ = "\nIn your program's main, call `airlock.set_config` and provide\na configuration object that follows the below format.\n\n{\n    'client_secrets_path': client_secrets_path,\n    'scopes': airlock.config.Defaults.OAUTH_SCOPES,\n    'xsrf_cookie_name': airlock.config.Defaults.Xsrf.COOKIE_NAME,\n    'policies': {\n        'csp': airlock.config.Defaults.Policies.CSP,\n        'frame_options': airlock.config.Defaults.XFrameOptions.SAMEORIGIN,\n        'hsts': airlock.config.Defaults.Policies.HSTS,\n    },\n    'webapp2_extras.auth': {\n        'token_cache_age': airlock.config.Defaults.Xsrf.TOKEN_AGE,\n        'token_max_age': airlock.config.Defaults.Xsrf.TOKEN_AGE,\n        'token_new_age': airlock.config.Defaults.Xsrf.TOKEN_AGE,\n        'user_model': '<path.to.user.model.subclass.User>',\n    },\n    'webapp2_extras.sessions': {\n        'secret_key': '<secret_key>',\n        'user_model': '<path.to.user.model.subclass.User>',\n    },\n}\n"
import os
__all__ = [
 'set_config',
 'Defaults']
_airlock_config = None

class Error(Exception):
    pass


class ConfigError(Error, ValueError):
    pass


def set_config(config):
    global _airlock_config
    if 'webapp2_extras.sessions' not in config:
        config['webapp2_extras.sessions'] = {}
    if 'cookie_args' not in config['webapp2_extras.sessions']:
        config['webapp2_extras.sessions']['cookie_args'] = {}
    config['webapp2_extras.sessions']['cookie_args']['httponly'] = True
    _is_secure = os.getenv('wsgi.url_scheme', '') == 'https'
    config['webapp2_extras.sessions']['cookie_args']['secure'] = _is_secure
    if 'webapp2_extras.auth' not in config:
        config['webapp2_extras.auth'] = {}
    if 'token_cache_age' not in config['webapp2_extras.auth']:
        config['webapp2_extras.auth']['token_cache_age'] = Defaults.Xsrf.TOKEN_AGE
    if 'token_max_age' not in config['webapp2_extras.auth']:
        config['webapp2_extras.auth']['token_max_age'] = Defaults.Xsrf.TOKEN_AGE
    if 'token_new_age' not in config['webapp2_extras.auth']:
        config['webapp2_extras.auth']['token_new_age'] = Defaults.Xsrf.TOKEN_AGE
    _airlock_config = config


def get_config():
    return _airlock_config


class Defaults(object):

    class Xsrf(object):
        COOKIE_NAME = 'XSRF_TOKEN'
        TOKEN_AGE = 604800

    class XFrameOptions(object):
        DENY = 'DENY'
        SAMEORIGIN = 'SAMEORIGIN'

    class Policies(object):
        CSP = None
        HSTS = {'max_age': 2592000, 'includeSubdomains': True}

    OAUTH_SCOPES = [
     'https://www.googleapis.com/auth/userinfo.email',
     'https://www.googleapis.com/auth/userinfo.profile']
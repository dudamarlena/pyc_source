# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/authz.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 2320 bytes
"""Authorization for Treadmill API."""
import logging, importlib, decorator
_LOGGER = logging.getLogger(__name__)

class AuthorizationError(Exception):
    __doc__ = 'Authorization error.'

    def __init__(self, annotations):
        self.annotations = annotations
        super(AuthorizationError, self).__init__('\n'.join(self.annotations))


class NullAuthorizer(object):
    __doc__ = 'Passthrough authorization class.'

    def __init__(self):
        pass

    def authorize(self, _resource, _action, _args, _kwargs):
        """Null authorization - always succeeds."""
        pass


class PluginAuthorizer(object):
    __doc__ = 'Loads authorizer implementation plugin.'

    def __init__(self, user_clbk):
        self.impl = None
        try:
            authzmod = importlib.import_module('treadmill.plugins.api.authz')
            self.impl = authzmod.init(user_clbk)
        except ImportError as err:
            _LOGGER.warn('Unable to load auth plugin: %s', err)

    def authorize(self, resource, action, args, kwargs):
        """Delegate authorization to the plugin."""
        if not self.impl:
            return False
        return self.impl.authorize(resource, action, args, kwargs)


def authorize(authorizer):
    """Constructs authorizer decorator."""

    @decorator.decorator
    def decorated(func, *args, **kwargs):
        """Decorated function."""
        action = getattr(func, 'auth_action', func.__name__.strip('_'))
        resource = getattr(func, 'auth_resource', func.__module__.strip('_'))
        _LOGGER.debug('Authorize: %s %s %r %r', resource, action, args, kwargs)
        authorizer.authorize(resource, action, args, kwargs)
        return func(*args, **kwargs)

    return decorated


def wrap(api, authorizer):
    """Returns module API wrapped with authorizer function."""
    for action in dir(api):
        if action.startswith('_'):
            continue
        if authorizer:
            auth = authorize(authorizer)
            attr = getattr(api, action)
            if hasattr(attr, '__call__'):
                setattr(api, action, auth(attr))
            else:
                if hasattr(attr, '__init__'):
                    setattr(api, action, wrap(attr, authorizer))
                else:
                    _LOGGER.want('unknown attribute type: %r, %s', api, action)
                    continue

    return api
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/keyring/keyring/backend.py
# Compiled at: 2020-01-10 16:25:34
# Size of source mod 2**32: 6337 bytes
"""
Keyring implementation support
"""
import os, abc, logging, operator
try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata

from . import credentials, errors, util
from .util import properties
__metaclass__ = type
log = logging.getLogger(__name__)
by_priority = operator.attrgetter('priority')
_limit = None

class KeyringBackendMeta(abc.ABCMeta):
    __doc__ = "\n    A metaclass that's both an ABCMeta and a type that keeps a registry of\n    all (non-abstract) types.\n    "

    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        if not hasattr(cls, '_classes'):
            cls._classes = set()
        classes = cls._classes
        if not cls.__abstractmethods__:
            classes.add(cls)


class KeyringBackend(metaclass=KeyringBackendMeta):
    __doc__ = 'The abstract base class of the keyring, every backend must implement\n    this interface.\n    '

    def priority(cls):
        """
        Each backend class must supply a priority, a number (float or integer)
        indicating the priority of the backend relative to all other backends.
        The priority need not be static -- it may (and should) vary based
        attributes of the environment in which is runs (platform, available
        packages, etc.).

        A higher number indicates a higher priority. The priority should raise
        a RuntimeError with a message indicating the underlying cause if the
        backend is not suitable for the current environment.

        As a rule of thumb, a priority between zero but less than one is
        suitable, but a priority of one or greater is recommended.
        """
        pass

    @properties.ClassProperty
    @classmethod
    def viable(cls):
        with errors.ExceptionRaisedContext() as (exc):
            cls.priority
        return not bool(exc)

    @classmethod
    def get_viable_backends(cls):
        """
        Return all subclasses deemed viable.
        """
        return filter(operator.attrgetter('viable'), cls._classes)

    @properties.ClassProperty
    @classmethod
    def name(cls):
        """
        The keyring name, suitable for display.

        The name is derived from module and class name.
        """
        parent, sep, mod_name = cls.__module__.rpartition('.')
        mod_name = mod_name.replace('_', ' ')
        return ' '.join([mod_name, cls.__name__])

    def __str__(self):
        keyring_class = type(self)
        return '{}.{} (priority: {:g})'.format(keyring_class.__module__, keyring_class.__name__, keyring_class.priority)

    @abc.abstractmethod
    def get_password(self, service, username):
        """Get password of the username for the service
        """
        pass

    @abc.abstractmethod
    def set_password(self, service, username, password):
        """Set password for the username of the service.

        If the backend cannot store passwords, raise
        NotImplementedError.
        """
        raise errors.PasswordSetError('reason')

    def delete_password(self, service, username):
        """Delete the password for the username of the service.

        If the backend cannot store passwords, raise
        NotImplementedError.
        """
        raise errors.PasswordDeleteError('reason')

    def get_credential(self, service, username):
        """Gets the username and password for the service.
        Returns a Credential instance.

        The *username* argument is optional and may be omitted by
        the caller or ignored by the backend. Callers must use the
        returned username.
        """
        if username is not None:
            password = self.get_password(service, username)
            if password is not None:
                return credentials.SimpleCredential(username, password)

    def set_properties_from_env(self):
        """For all KEYRING_PROPERTY_* env var, set that property."""

        def parse(item):
            key, value = item
            pre, sep, name = key.partition('KEYRING_PROPERTY_')
            return sep and (name.lower(), value)

        props = filter(None, map(parse, os.environ.items()))
        for name, value in props:
            setattr(self, name, value)


class Crypter:
    __doc__ = 'Base class providing encryption and decryption\n    '

    @abc.abstractmethod
    def encrypt(self, value):
        """Encrypt the value.
        """
        pass

    @abc.abstractmethod
    def decrypt(self, value):
        """Decrypt the value.
        """
        pass


class NullCrypter(Crypter):
    __doc__ = 'A crypter that does nothing\n    '

    def encrypt(self, value):
        return value

    def decrypt(self, value):
        return value


def _load_plugins():
    """
    Locate all setuptools entry points by the name 'keyring backends'
    and initialize them.
    Any third-party library may register an entry point by adding the
    following to their setup.py::

        entry_points = {
            'keyring.backends': [
                'plugin_name = mylib.mymodule:initialize_func',
            ],
        },

    `plugin_name` can be anything, and is only used to display the name
    of the plugin at initialization time.

    `initialize_func` is optional, but will be invoked if callable.
    """
    entry_points = metadata.entry_points()['keyring.backends']
    for ep in entry_points:
        try:
            log.info('Loading %s', ep.name)
            init_func = ep.load()
            if callable(init_func):
                init_func()
        except Exception:
            log.exception(('Error initializing plugin {ep}.'.format)(**locals()))


@util.once
def get_all_keyring():
    """
    Return a list of all implemented keyrings that can be constructed without
    parameters.
    """
    _load_plugins()
    viable_classes = KeyringBackend.get_viable_backends()
    rings = util.suppress_exceptions(viable_classes, exceptions=TypeError)
    return list(rings)
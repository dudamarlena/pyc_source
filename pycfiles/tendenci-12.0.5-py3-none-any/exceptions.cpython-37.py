# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/registry/exceptions.py
# Compiled at: 2020-02-26 14:47:58
# Size of source mod 2**32: 840 bytes
__ALL__ = ['AlreadyRegistered',
 'NotRegistered',
 'FieldNotAllowed',
 'FieldError',
 'PackageImportError']

class RegistryError(Exception):
    __doc__ = '\n    Base exception for the registry app\n    '


class AlreadyRegistered(RegistryError):
    __doc__ = '\n    Raise when model is already registered with the site\n    '


class NotRegistered(RegistryError):
    __doc__ = '\n    Raise when model is not registered with the site\n    '


class FieldNotAllowed(RegistryError):
    __doc__ = '\n    Raise when field in registry is not in allowed fields\n    '


class FieldError(RegistryError):
    __doc__ = '\n    Raise when field in registry is of the wrong type\n    '


class PackageImportError(RegistryError):
    __doc__ = '\n    Raise when the packages list in the apps registry fails to import\n    '
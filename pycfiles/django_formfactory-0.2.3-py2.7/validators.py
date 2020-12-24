# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/validators.py
# Compiled at: 2017-09-07 07:30:48
from formfactory import _registry
from formfactory.utils import auto_registration, clean_key

def register(func):
    key = clean_key(func)
    _registry['validators'][key] = func

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def unregister(func):
    key = clean_key(func)
    if key in _registry['validators']:
        del _registry['validators'][key]


def get_registered_validators():
    return _registry['validators']


def auto_discover():
    """Perform discovery of validator functions over all other installed apps.
    """
    auto_registration('validators')
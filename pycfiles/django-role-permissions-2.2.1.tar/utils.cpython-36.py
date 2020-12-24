# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/filipeximenes/Projects/django-role-permissions/rolepermissions/utils.py
# Compiled at: 2018-12-02 07:23:05
# Size of source mod 2**32: 851 bytes
from __future__ import unicode_literals
import re, collections

def user_is_authenticated(user):
    if isinstance(user.is_authenticated, collections.Callable):
        authenticated = user.is_authenticated()
    else:
        authenticated = user.is_authenticated
    return authenticated


def camelToSnake(s):
    """
    https://gist.github.com/jaytaylor/3660565
    Is it ironic that this function is written in camel case, yet it
    converts to snake case? hmm..
    """
    _underscorer1 = re.compile('(.)([A-Z][a-z]+)')
    _underscorer2 = re.compile('([a-z0-9])([A-Z])')
    subbed = _underscorer1.sub('\\1_\\2', s)
    return _underscorer2.sub('\\1_\\2', subbed).lower()


def snake_to_title(s):
    return ' '.join(x.capitalize() for x in s.split('_'))


def camel_or_snake_to_title(s):
    return snake_to_title(camelToSnake(s))
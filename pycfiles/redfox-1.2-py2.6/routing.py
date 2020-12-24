# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/redfox/routing.py
# Compiled at: 2009-10-20 11:31:07
"""Provides routable-endpoint manipulations, including the ``@route``,
``@get``, ``@post``, ``@put``, and ``@delete`` decorators.
"""
from functools import partial

def make_routable(target):
    """Ensures that a target is routable. If the target is already
    routable, nothing happens.
    """
    if not is_routable(target):
        target.__rule_args__ = []


def is_routable(target):
    """Returns ``True`` if and only if the passed target is routable."""
    return hasattr(target, '__rule_args__')


def routes(target, *extra_args, **extra_kwargs):
    """Retrieves the route definitions for a target, optionally adding
    extra parameters to each route. If called on a non-routable target,
    returns an empty sequence; otherwise, returns a sequence of
    ``(arg, kwarg)`` tuples, one for each route."""
    if is_routable(target):
        for (args, kwargs) in target.__rule_args__:
            yield (
             args + extra_args, dict(kwargs, **extra_kwargs))


def route(*args, **kwargs):
    """Creates a decorator that makes target objects routable. The
    parameters passed to ``@route`` will be stored in the new route
    definition and returned by ``routes(target)``.
    """

    def decorate_target(target):
        make_routable(target)
        target.__rule_args__.append((args, kwargs))
        return target

    return decorate_target


get = partial(route, methods=['GET'])
post = partial(route, methods=['POST'])
put = partial(route, methods=['PUT'])
delete = partial(route, methods=['DELETE'])
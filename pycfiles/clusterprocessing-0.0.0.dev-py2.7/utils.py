# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fabfile/utils.py
# Compiled at: 2013-10-25 00:17:01
"""Utilities"""
from functools import wraps
from imp import find_module
from contextlib import contextmanager
from fabric.api import abort, hide, local, puts, quiet, settings, warn

def tobool(s):
    if isinstance(s, bool):
        return s
    return s.lower() in ('yes', 'y')


def toint(s):
    if isinstance(s, int):
        return s
    return int(s)


@contextmanager
def msg(s):
    """Print message given as ``s`` in a context manager

    Prints "{s} ... OK"
    """
    puts(('{0:s} ... ').format(s), end='', flush=True)
    with settings(hide('everything')):
        yield
    puts('OK', show_prefix=False, flush=True)


def pip(*args, **kwargs):
    requirements = kwargs.get('requirements', None)
    if requirements is not None:
        local(('pip install -U -r {0:s}').format(kwargs['requirements']))
    else:
        args = list(arg for arg in args if not has_module(arg))
        if args:
            local(('pip install {0:s}').format((' ').join(args)))
    return


def has_module(name):
    try:
        return find_module(name)
    except ImportError:
        return False


def has_binary(name):
    with quiet():
        return local(('which {0:s}').format(name)).succeeded


def requires(*names, **kwargs):
    """Decorator/Wrapper that aborts if not all requirements are met.

    Aborts if not all requirements are met given a test function (defaulting to :func:`~has_binary`).

    :param kwargs: Optional kwargs. e.g: ``test=has_module``
    :type kwargs: dict

    :returns: None or aborts
    :rtype: None
    """
    test = kwargs.get('test', has_binary)

    def decorator(f):

        @wraps(f)
        def wrapper(*args, **kwds):
            if all(test(name) for name in names):
                return f(*args, **kwds)
            for name in names:
                if not test(name):
                    warn(('{0:s} not found').format(name))

            abort(('requires({0:s}) failed').format(repr(names)))

        return wrapper

    return decorator
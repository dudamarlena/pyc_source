# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/sockfilter/sockfilter/__init__.py
# Compiled at: 2014-07-08 16:23:45
__all__ = ['Address', 'SockFilterError', 'enable', 'disable', 'is_enabled',
 'sockfiltering', 'with_sockfiltering']
from contextlib import contextmanager
import functools
from .address import Address
from .error import SockFilterError
from . import real, fake

def is_enabled():
    return fake.instance is not None


def enable(predicate):
    if is_enabled():
        disable()
    fake.instance = fake.Fake(predicate)
    fake.instance.apply()


def disable():
    if not is_enabled():
        return
    else:
        real.restore()
        fake.instance = None
        return


@contextmanager
def sockfiltering(*args, **kwargs):
    try:
        enable(*args, **kwargs)
        yield
    finally:
        disable()


def with_sockfiltering(*args, **kwargs):

    def decorate(f):

        @functools.wraps(f)
        def wrapped(*wrapped_args, **wrapped_kwargs):
            with sockfiltering(*args, **kwargs):
                return f(*wrapped_args, **wrapped_kwargs)

        return wrapped

    return decorate
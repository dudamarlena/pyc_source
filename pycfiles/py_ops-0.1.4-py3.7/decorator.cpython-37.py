# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyops\decorator.py
# Compiled at: 2020-04-17 11:44:33
# Size of source mod 2**32: 1147 bytes
import functools

def make(key='flow'):

    def make_key(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        if hasattr(wrapper, 'ah_type'):
            wrapper.ah_type.append(key)
        else:
            wrapper.ah_type = [
             key]
        if key in ('flow', 'check', 'setup', 'teardown'):
            wrapper.argcount = func.__code__.co_argcount
        return wrapper

    return make_key


make_setup_class = make(key='setup_class')
make_setup = make(key='setup')
make_data = make(key='data')
make_flow = make(key='flow')
make_check = make(key='check')
make_teardown = make(key='teardown')
make_teardown_class = make(key='teardown_class')

def alias(name=None):

    def make_alias(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.alias = name
        return wrapper

    return make_alias
# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wc4nin/.cache/pypoetry/virtualenvs/snakypy-Jn9yRLD4-py3.8/lib/python3.8/site-packages/snakypy/utils/decorators.py
# Compiled at: 2020-03-21 13:31:27
# Size of source mod 2**32: 1239 bytes
import os
from functools import wraps

def denying_os(os_name):
    """Decorator to ban an operating system from software through os.name.

    Arguments:
        **os_name** {str} - You must receive the os.name of the operating system to be banned.
                            Windows = nt
                            Linux/Mac OS = posix
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            if os.name == os_name:
                msg = f"This software is not compatible with this ({os_name}) operating system."
                raise Exception(msg)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def only_for_linux(func):
    """A decorator to force a function or method to run on Unix systems only."""
    import platform

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not platform.system() == 'Linux':
            msg = f'Invalid operating system. This function "{func.__name__}" is only compatible with Linux systems.'
            raise Exception(msg)
        return func(*args, **kwargs)

    return wrapper


__all__ = [
 'only_for_linux', 'denying_os']
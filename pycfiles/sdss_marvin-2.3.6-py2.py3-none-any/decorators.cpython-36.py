# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Brian/Work/github_projects/marvin_pypi/python/marvin/extern/marvin_brain/python/brain/utils/general/decorators.py
# Compiled at: 2018-03-20 20:19:12
# Size of source mod 2**32: 1877 bytes
from functools import wraps
from brain.core.exceptions import BrainError
from brain import bconfig
try:
    from sdss_access.path import Path
except ImportError:
    Path = None

__all__ = [
 'parseRoutePath', 'checkPath']

def parseRoutePath(f):
    """ Decorator to parse generic route path """

    @wraps(f)
    def decorated_function(inst, *args, **kwargs):
        if 'path' in kwargs:
            if kwargs['path']:
                for kw in kwargs['path'].split('/'):
                    if len(kw) == 0:
                        pass
                    else:
                        var, value = kw.split('=')
                        kwargs[var] = value

        kwargs.pop('path')
        return f(inst, *args, **kwargs)

    return decorated_function


def checkPath(func):
    """Decorator that checks if sdss_access Path has been imported """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not Path:
            raise BrainError('sdss_access is not installed')
        else:
            return func(*args, **kwargs)

    return wrapper


def check_auth(func):
    """ Decorator that checks if a valid netrc file exists

    Function Decorator to check if a valid netrc file exists.
    If not it raises an error.  Otherwise it
    returns the function and proceeds as normal.

    Returns:
        The decorated function

    Raises:
        BrainError: You are not authorized to access the SDSS collaboration

    Example:
        >>>
        >>> @check_auth
        >>> def my_function():
        >>>     return 'I am working function'
        >>>

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        valid_netrc = bconfig._check_netrc()
        if valid_netrc:
            return func(*args, **kwargs)
        raise BrainError('You are not authorized to access the SDSS collaboration')

    return wrapper
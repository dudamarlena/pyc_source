# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/utils/util.py
# Compiled at: 2017-06-30 11:16:28
# Size of source mod 2**32: 1014 bytes
import contextlib, warnings, functools
from mongoengine.errors import FieldDoesNotExist, ValidationError
from flask_restframework import exceptions

@contextlib.contextmanager
def wrap_mongoengine_errors(updater=None):
    try:
        yield
    except (FieldDoesNotExist, ValidationError) as e:
        data = e.to_dict()
        if updater:
            data = updater(data)
        raise exceptions.ValidationError(data)


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used."""

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)
        warnings.warn('Call to deprecated function {}.'.format(func.__name__), category=DeprecationWarning, stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)
        return func(*args, **kwargs)

    return new_func
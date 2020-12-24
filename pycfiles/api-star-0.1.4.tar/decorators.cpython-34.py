# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tomchristie/GitHub/api-star/api_star/decorators.py
# Compiled at: 2016-04-14 12:17:44
# Size of source mod 2**32: 2328 bytes
from api_star.compat import copy_signature, getargspec
from api_star.exceptions import ValidationError
from functools import wraps

def validate(**validated):
    """
    1. The `validate()` function itself takes keyword arguments,
       and returns a decorator.
    """

    def decorator(func):
        """
        2. The decorator is called on the function that `@validate()` has been
           applied too, and returns the updated function.
        """
        arg_names = getargspec(func).args
        for key in validated.keys():
            if key not in arg_names:
                raise RuntimeError('"%s" keyword argument to @validate() decorator does not match any arguments in the function signature of %s' % (
                 key, func))
                continue

        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            3. When a function decorated by `@validate()` is called, this
               wrapper function is what actaully gets executed.
            """
            for idx, value in enumerate(args):
                key = arg_names[idx]
                kwargs[key] = value

            errors = {}
            for key, value in kwargs.items():
                if key in validated:
                    validator = validated[key]
                    try:
                        kwargs[key] = validator(value)
                    except ValidationError as exc:
                        errors[key] = exc.description

                    continue

            if errors:
                raise ValidationError(errors)
            return func(**kwargs)

        copy_signature(func, wrapper)
        return wrapper

    return decorator


def annotate(**kwargs):

    def decorator(func):
        for key, value in kwargs.items():
            setattr(func, key, value)

        return func

    return decorator
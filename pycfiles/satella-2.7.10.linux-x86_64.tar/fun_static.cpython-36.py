# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/coding/fun_static.py
# Compiled at: 2020-04-14 13:42:23
# Size of source mod 2**32: 479 bytes


def static_var(var_name: str, starting_value=None):
    """
    Declare a static variable for given function

    Use it like:

    >>> @static_var('counter', 2)
    >>> def count():
    >>>     count.counter += 1

    or:

    >>> class MyClass:
    >>>     @static_var('counter', 2)
    >>>     def count(self):
    >>>         MyClass.count.counter += 1
    """

    def decorate(func):
        setattr(func, var_name, starting_value)
        return func

    return decorate
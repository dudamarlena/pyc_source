# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/dataql/utils.py
# Compiled at: 2015-06-15 16:21:11
# Size of source mod 2**32: 1049 bytes
"""``utils`` module of ``dataql``.

Provide some simple utilities.

"""

def class_repr(value):
    """Returns a representation of the value class.

    Arguments
    ---------
    value
        A class or a class instance

    Returns
    -------
    str
        The "module.name" representation of the value class.

    Example
    -------
    >>> from datetime import date
    >>> class_repr(date)
    'datetime.date'
    >>> class_repr(date.today())
    'datetime.date'
    """
    klass = value
    if not isinstance(value, type):
        klass = klass.__class__
    return '.'.join([klass.__module__, klass.__name__])


def isclass(value):
    """Tell if the value is a class or not.

    Arguments
    ---------
    value
        Value to test if its a class or not.

    Returns
    -------
    boolean
        ``True`` if the value is a class, ``False`` otherwise.

    Example
    -------

    >>> from datetime import date
    >>> isclass(date)
    True
    >>> isclass(date.today())
    False

    """
    return isinstance(value, type)
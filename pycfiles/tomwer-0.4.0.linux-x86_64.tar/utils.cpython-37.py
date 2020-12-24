# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/utils.py
# Compiled at: 2019-12-11 09:05:54
# Size of source mod 2**32: 2582 bytes
__authors__ = [
 'H. Payno', 'T. Vincent']
__license__ = 'MIT'
__date__ = '04/01/2018'
import functools

def addHTMLLine(txt):
    return '<li>' + txt + '</li>'


def _docstring(dest, origin):
    """Implementation of docstring decorator.

    It patches dest.__doc__.
    """
    if not isinstance(dest, type):
        if isinstance(origin, type):
            try:
                origin = getattr(origin, dest.__name__)
            except AttributeError:
                raise ValueError('origin class has no %s method' % dest.__name__)

    dest.__doc__ = origin.__doc__
    return dest


def docstring(origin):
    """Decorator to initialize the docstring from another source.

    This is useful to duplicate a docstring for inheritance and composition.

    If origin is a method or a function, it copies its docstring.
    If origin is a class, the docstring is copied from the method
    of that class which has the same name as the method/function
    being decorated.

    :param origin:
        The method, function or class from which to get the docstring
    :raises ValueError:
        If the origin class has not method n case the
    """
    return functools.partial(_docstring, origin=origin)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.macosx-10.6-intel-2.7/spherogram/sage_helper.py
# Compiled at: 2017-05-26 08:26:49
"""
Helper code for dealing with additional functionality when Sage is
present.

Any method which works only in Sage should be decorated with
"@sage_method" and any doctests (in Sage methods or not) which should
be run only in Sage should be styled with input prompt "sage:" rather
than the usual ">>>".

Similarly, doctests which require SnapPy should be styled in a block
where the first non-whitespace character is | followed by a space.
"""
try:
    import sage.all
    _within_sage = True
except:
    _within_sage = False
    import decorator

import doctest, re, types

class SageNotAvailable(Exception):
    pass


if _within_sage:

    def sage_method(function):
        function._sage_method = True
        return function


else:

    def _sage_method(function, *args, **kw):
        raise SageNotAvailable('Sorry, this feature requires using SnapPy inside Sage.')


    def sage_method(function):
        return decorator.decorator(_sage_method, function)
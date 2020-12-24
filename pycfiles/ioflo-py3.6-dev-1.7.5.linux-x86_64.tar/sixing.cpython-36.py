# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/aid/sixing.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 1131 bytes
"""
Python 2 to 3 supporting definitions

"""
from __future__ import absolute_import, division, print_function
import sys
if sys.version > '3':
    long = int
    basestring = (str, bytes)
    unicode = str
    xrange = range

    def ns2b(x):
        """
        Converts from native str type to native bytes type
        """
        return x.encode('ISO-8859-1')


    def ns2u(x):
        """
        Converts from native str type to native unicode type
        """
        return x


    def reraise(kind, value, trace=None):
        if value is None:
            value = kind()
        if value.__traceback__ is not trace:
            raise value.with_traceback(trace)
        raise value


else:

    def ns2b(x):
        """
        Converts from native str type to native bytes type
        """
        return x


    def ns2u(x):
        """
        Converts from native str type to native unicode type
        """
        return unicode(x)


    exec('def reraise(kind, value, trace=None): raise kind, value, trace', globals())
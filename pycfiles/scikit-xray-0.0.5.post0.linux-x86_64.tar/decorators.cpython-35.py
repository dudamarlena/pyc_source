# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/testing/decorators.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 4461 bytes
"""
This module is for decorators related to testing.

Much of this code is inspired by the code in matplotlib.  Exact copies
are noted.
"""
from skxray.testing.noseclasses import KnownFailureTest, KnownFailureDidNotFailTest
import nose
from nose.tools import make_decorator

def known_fail_if(cond):
    """
    Make sure a known failure fails.

    This function is a decorator factory.
    """

    def dec(in_func):
        if cond:

            def inner_wrap():
                try:
                    in_func()
                except Exception:
                    raise KnownFailureTest()
                else:
                    raise KnownFailureDidNotFailTest()

            return make_decorator(in_func)(inner_wrap)
        else:
            return in_func

    return dec


def skip_if(cond, msg=''):
    """
    A decorator to skip a test if condition is met
    """

    def dec(in_func):
        if cond:

            def wrapper():
                raise nose.SkipTest(msg)

            return make_decorator(in_func)(wrapper)
        else:
            return in_func

    return dec
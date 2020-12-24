# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/waferslim/specs/spec_classes.py
# Compiled at: 2010-02-17 15:03:13
"""
Simplistic classes and functions for use only in specs
"""

class ClassWithNoArgs(object):
    """ A class to instantiate with a no-arg constructor"""
    pass


class ClassWithOneArg(object):
    """ A class to instantiate with a one-arg constructor"""

    def __init__(self, arg):
        pass


class ClassWithTwoArgs(object):
    """ A class to instantiate with a two-arg constructor"""

    def __init__(self, arg1, arg2):
        pass


class _Parrot(object):
    """ A class to use as an underlying system under test """

    def is_dead(self):
        return False


class ClassWithSystemUnderTestMethod(object):
    """ A class that wishes to expose an underlying sut """

    def sut(self):
        return _Parrot()


class ClassWithSystemUnderTestField(object):
    """ Another class that wishes to expose an underlying sut """

    def __init__(self):
        self.sut = _Parrot()
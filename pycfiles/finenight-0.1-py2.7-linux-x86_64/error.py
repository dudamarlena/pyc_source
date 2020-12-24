# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/finenight/error.py
# Compiled at: 2014-08-29 00:09:34


class Error:

    def __init__(self, string):
        self.string = string

    def __str__(self):
        return self.string


class StateError(Error):
    """This error is raised when a state is invalid"""
    pass


class AlphabetError(Error):
    """This error is raised when the alphabet of a FSA is invalid"""
    pass


class ConstructionError(Error):
    """This error is raised when we encounter a problem when
    construction a FSA.
    """
    pass


class NotImplemented(Error):
    """This error is raised when the implementation of the function
    is incomplete
    """
    pass
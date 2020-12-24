# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/gittle/exceptions.py
# Compiled at: 2013-09-03 02:36:01


class InvalidRemoteUrl(Exception):
    """The url provided for the remote service is invalid"""
    pass


class InvalidRSAKey(Exception):
    """Can't generate key ..."""
    pass
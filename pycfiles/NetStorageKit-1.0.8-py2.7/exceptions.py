# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/netstoragekit/exceptions.py
# Compiled at: 2015-06-12 15:28:19


class NetStorageKitError(Exception):
    """Generic error in the stack.
    Mostly used as a wrapper of other exceptions, preserving the original info.
    """
    pass
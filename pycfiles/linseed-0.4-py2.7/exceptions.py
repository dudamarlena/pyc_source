# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/linseed/exceptions.py
# Compiled at: 2011-01-15 05:51:47


class DataNotAvailable(Exception):
    """Thrown by plugins when they are instantiated and can not
    provide information about the system.

    For example, a WICD plugin could throw this if it's instantiated
    on a system that is not using WICD.
    """
    pass
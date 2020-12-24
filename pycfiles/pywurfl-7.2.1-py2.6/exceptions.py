# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pywurfl/exceptions.py
# Compiled at: 2011-01-06 14:57:56
"""
Exception Classes
"""
__author__ = 'Armand Lynch <lyncha@users.sourceforge.net>'
__copyright__ = 'Copyright 2006-2011, Armand Lynch'
__license__ = 'LGPL'
__url__ = 'http://celljam.net/'

class WURFLException(Exception):
    """
    pywurfl base exception class.
    """
    pass


class ExistsException(WURFLException):
    """
    General exception class

    Raised when an operation should not continue if an object exists.
    """
    pass


class DeviceNotFound(WURFLException):
    """
    Device Not Found exception class

    Raised when pywurfl cannot find a device by using either select_*
    API functions.
    """
    pass


class ActualDeviceRootNotFound(WURFLException):
    """
    Actual Device Root Not Found exception class

    Raised when pywurfl cannot find an actual device root by using either
    select_* API functions.
    """
    pass
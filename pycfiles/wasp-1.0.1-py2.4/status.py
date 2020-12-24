# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wasp/status.py
# Compiled at: 2008-09-17 11:14:28
"""
This module contains constants for statuses returned in notifications
from WASPs about the delivery of messages sent wit hteh `send`
function.

They are implemented as classes in case they need to be adapted using
the component architecture at a later date.
"""

class Status:
    __module__ = __name__


class Delivered(Status):
    """
    The message was successfully delivered to its recipient.
    """
    __module__ = __name__


class Failed(Status):
    """
    The message delivery has failed.
    """
    __module__ = __name__


delivered = Delivered()
failed = Failed()
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/ZScheduler/interfaces/ITimer.py
# Compiled at: 2015-07-18 19:40:58
from zope.interface import Interface

class ITimer(Interface):
    """
    interface a timer must conform to - observer pattern ...
    """

    def __init__(self):
        """
        default constructor
        """
        pass

    def start(semaphore):
        """
        begin event scheduling
        accepting a threading.Event to notify scheduling changes
        """
        pass

    def stop():
        """
        end event scheduling
        """
        pass

    def isActive():
        """
        verify whether or not the timer is actually installed/running at it's
        underlying level
        """
        pass
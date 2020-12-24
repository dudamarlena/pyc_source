# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/ZScheduler/interfaces/IQueue.py
# Compiled at: 2015-07-18 19:40:58
from zope.interface import Interface

class IQueue(Interface):
    """
    a queue of ZScheduleEvents
    """

    def pop(url):
        """
        remove url from queue
        """
        pass

    def push(url, event):
        """
        place url/event in queue
        """
        pass

    def reload():
        """
        scan ZODB placing all ZScheduleEvent's in queue
        """
        pass

    def get(url):
        """
        return the ZScheduleEvent
        """
        pass

    def getEvents(times):
        """
        get events scheduled between times
        """
        pass
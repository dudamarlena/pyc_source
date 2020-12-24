# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/contentsync/events.py
# Compiled at: 2009-05-11 14:25:19
from zope.interface import implements
from interfaces import ISynchronizeStateChangeEvent

class SynchronizeStateChangeEvent(object):
    __module__ = __name__
    implements(ISynchronizeStateChangeEvent)

    def __init__(self, object):
        self.object = object
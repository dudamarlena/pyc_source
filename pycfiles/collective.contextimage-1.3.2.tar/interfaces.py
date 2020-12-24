# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/contentsync/interfaces.py
# Compiled at: 2009-05-11 14:25:19
from zope.component.interfaces import IObjectEvent

class ISynchronizeStateChangeEvent(IObjectEvent):
    """ 
    An event triggered by an utility which implements
    ISynchronizer
    """
    __module__ = __name__
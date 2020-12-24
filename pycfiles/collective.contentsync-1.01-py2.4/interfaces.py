# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/contentsync/interfaces.py
# Compiled at: 2009-05-11 14:25:19
from zope.component.interfaces import IObjectEvent

class ISynchronizeStateChangeEvent(IObjectEvent):
    """ 
    An event triggered by an utility which implements
    ISynchronizer
    """
    __module__ = __name__
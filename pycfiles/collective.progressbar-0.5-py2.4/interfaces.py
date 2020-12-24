# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/progressbar/interfaces.py
# Compiled at: 2009-09-18 14:53:56
from zope.component.interfaces import IObjectEvent
from zope.interface import Interface

class IInitialiseProgressBar(IObjectEvent):
    """ An event fired to initialise progress bar
    """
    __module__ = __name__


class IUpdateProgressEvent(IObjectEvent):
    """ An event fired to update progress
    """
    __module__ = __name__
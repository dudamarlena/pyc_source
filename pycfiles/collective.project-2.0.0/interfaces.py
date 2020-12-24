# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
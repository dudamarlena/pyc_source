# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/synchro/interfaces/events.py
# Compiled at: 2008-12-16 18:21:20
from zope.interface import Interface
from collective.synchro import config
if config.HAS_PLONE3:
    from zope.lifecycleevent.interfaces import IObjectEvent
else:
    from zope.app.event.interfaces import IObjectEvent

class ISynchroModifiedEvent(IObjectEvent):
    """ marker interface for a  modified synchro event """
    __module__ = __name__


class ISynchroDeletedEvent(IObjectEvent):
    """ marker innterface for a delete synchro event """
    __module__ = __name__
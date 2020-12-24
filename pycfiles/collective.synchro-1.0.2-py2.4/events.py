# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
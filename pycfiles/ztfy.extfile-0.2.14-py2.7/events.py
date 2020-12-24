# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/extfile/events.py
# Compiled at: 2013-12-18 12:18:44
__docformat__ = 'restructuredtext'
import transaction
from zope.lifecycleevent.interfaces import IObjectModifiedEvent, IObjectAddedEvent, IObjectRemovedEvent
from ztfy.extfile.interfaces import IBaseExtFileInfo, IExtFileModifiedEvent, IExtFileAfterAddedEvent, IExtFileAfterModifiedEvent
from zope.component import adapter
from zope.component.interfaces import ObjectEvent
from zope.event import notify
from zope.interface import implements
from zope.lifecycleevent import ObjectModifiedEvent

class ExtFileModifiedEvent(ObjectModifiedEvent):
    implements(IExtFileModifiedEvent)


class ExtFileAfterAddedEvent(ObjectEvent):
    implements(IExtFileAfterAddedEvent)


class ExtFileAfterModifiedEvent(ObjectEvent):
    implements(IExtFileAfterModifiedEvent)


def _commitDeletedExtFile(status, object):
    if status:
        object.commitDeletedFile()


@adapter(IBaseExtFileInfo, IObjectAddedEvent)
def handleNewExtFile(object, event):
    try:
        object.moveTempFile()
    except:
        object.deleteFile(temporary=True)
        transaction.get().addAfterCommitHook(_commitDeletedExtFile, kws={'object': object})
        raise

    notify(ExtFileAfterAddedEvent(object))


@adapter(IBaseExtFileInfo, IObjectModifiedEvent)
def handleModifiedExtFile(object, event):
    object.deleteFile()
    transaction.get().addAfterCommitHook(_commitDeletedExtFile, kws={'object': object})
    object.moveTempFile()
    notify(ExtFileAfterModifiedEvent(object))


@adapter(IBaseExtFileInfo, IObjectRemovedEvent)
def handleDeletedExtFile(object, event):
    object.deleteFile()
    transaction.get().addAfterCommitHook(_commitDeletedExtFile, kws={'object': object})
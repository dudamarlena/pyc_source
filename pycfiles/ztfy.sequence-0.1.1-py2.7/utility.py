# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/sequence/utility.py
# Compiled at: 2012-07-02 16:55:09
from zope.lifecycleevent.interfaces import IObjectAddedEvent, IObjectCopiedEvent, IObjectRemovedEvent
from ztfy.sequence.interfaces import ISequentialIntIds, ISequentialIdTarget, ISequentialIdInfo
from zope.component import adapter, queryUtility
from zope.interface import implements
from zope.intid import IntIds
from zope.schema.fieldproperty import FieldProperty

class SequentialIntIds(IntIds):
    """Sequential IDs utility"""
    implements(ISequentialIntIds)
    prefix = FieldProperty(ISequentialIntIds['prefix'])
    hex_oid_length = FieldProperty(ISequentialIntIds['hex_oid_length'])
    _lastId = 0

    def _generateId(self):
        self._lastId += 1
        return self._lastId

    def register(self, ob):
        if not ISequentialIdTarget.providedBy(ob):
            return None
        else:
            return super(SequentialIntIds, self).register(ob)

    def generateHexId(self, obj, oid):
        return '%%s%%s%%.%dx' % self.hex_oid_length % (self.prefix or '',
         getattr(obj, 'prefix', ''),
         oid)


@adapter(ISequentialIdTarget, IObjectAddedEvent)
def handleNewSequentialIdTarget(obj, event):
    """Set unique ID for each added object"""
    utility = queryUtility(ISequentialIntIds, getattr(obj, 'sequence_name', ''))
    if utility is not None:
        info = ISequentialIdInfo(obj)
        if not info.oid:
            oid = info.oid = utility.register(obj)
            info.hex_oid = utility.generateHexId(obj, oid)
    return


@adapter(ISequentialIdTarget, IObjectCopiedEvent)
def handleCopiedSequentialIdTarget(obj, event):
    """Reset unique ID when an object is copied"""
    info = ISequentialIdInfo(obj)
    info.oid = None
    info.hex_oid = None
    return


@adapter(ISequentialIdTarget, IObjectRemovedEvent)
def handleRemovedSequentialIdTarget(obj, event):
    """Unregister object when it is removed"""
    utility = queryUtility(ISequentialIntIds, getattr(obj, 'sequence_name', ''))
    if utility is not None and utility.queryId(obj) is not None:
        utility.unregister(obj)
    return
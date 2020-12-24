# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/brain.py
# Compiled at: 2008-09-11 19:48:09
from AccessControl import ModuleSecurityInfo
from Acquisition import aq_base
from Globals import InitializeClass
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.ReferenceEngine import Reference
from Products.Archetypes.utils import shasattr
from config import *
import brain, interfaces
modulesec = ModuleSecurityInfo('Products.Relations.brain')
modulesec.declarePublic('makeBrainAggregate')
_marker = ()

class BrainAggregate:
    """Catalog brain kind of object that aggregates metadata from multiple
    catalogs."""
    __module__ = __name__
    __implements__ = (
     interfaces.IBrainAggregate,)
    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(self, brain, sources):
        self.brain = brain
        self.sources = sources

    def __getitem__(self, key):
        attr = getattr(aq_base(self), key, _marker)
        if attr is not _marker:
            return getattr(self, key)
        else:
            raise KeyError, key

    def __getattr__(self, key):
        attr = getattr(aq_base(self.brain), key, _marker)
        if attr is not _marker:
            return getattr(self.brain, key)
        else:
            raise AttributeError, key

    def __repr__(self):
        return '<Brain aggregate with UID: %s, path: %s>' % (self.brain.UID, self.brain.getPath())

    def __eq__(self, other):
        if interfaces.IBrainAggregate.isImplementedBy(other):
            return self.brain.UID == other.brain.UID and self.sources == other.sources


def makeBrainAggregate(context, obj):
    """Returns a brain aggregate that corresponds to obj.

    obj may be either a UID string, a brain of uid_catalog or an aggregated
    brain."""
    if interfaces.IBrainAggregate.isImplementedBy(obj):
        return obj
    elif isinstance(obj, type('')):
        return makeBrainAggrFromUID(context, obj)
    elif shasattr(obj, 'getPath'):
        return makeBrainAggrFromBrain(context, obj)
    else:
        raise ValueError, 'Object %r must be either UID or brain.' % obj


def makeBrainAggrFromUID(context, uid, catalogs=None):
    uc = getToolByName(context, UID_CATALOG)
    brain = uc(UID=uid)[0]
    return makeBrainAggrFromBrain(context, brain, catalogs)


def makeBrainAggrFromBrain(context, brain, catalogs=None):
    if catalogs is None:
        at = getToolByName(context, 'archetype_tool')
        sources = at.getCatalogsByType(brain.portal_type)
    else:
        sources = [ getToolByName(context, cid) for cid in catalogs ]
    sources = [ s for s in sources if s.getId() != UID_CATALOG ]
    aggr = BrainAggregate(brain, [ s.getId() for s in sources ])
    portal_url = getToolByName(context, 'portal_url')
    abs_path = '/%s/%s' % (portal_url(relative=1), brain.getPath())
    for s in sources:
        try:
            aggr.__dict__.update(s.getMetadataForUID(abs_path))
        except KeyError:
            continue

    return aggr


class ReferenceWithBrains(Reference):
    __module__ = __name__
    __implements__ = interfaces.IReferenceWithBrains


proxies = {'getSourceBrain': lambda self: brain.makeBrainAggregate(self, self.sourceUID), 
   'getTargetBrain': lambda self: brain.makeBrainAggregate(self, self.targetUID), 
   'getSourceObject': lambda self: Reference.getSourceObject(self), 
   'getTargetObject': lambda self: Reference.getTargetObject(self)}

def makeProxyMethod(key, valueFun):

    def proxyMethod(self):
        attr_name = '_v_%s' % key
        if not shasattr(self, attr_name):
            setattr(self, attr_name, valueFun(self))
        return getattr(self, attr_name)

    return proxyMethod


for (key, valueFun) in proxies.items():
    setattr(ReferenceWithBrains, key, makeProxyMethod(key, valueFun))

InitializeClass(ReferenceWithBrains)
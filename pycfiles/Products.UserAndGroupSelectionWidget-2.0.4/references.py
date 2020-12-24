# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/UpfrontContacts/references.py
# Compiled at: 2010-03-10 13:47:45
from Products.Archetypes.ReferenceEngine import Reference
from Products.Archetypes.exceptions import ReferenceException

class BidirectionalReference(Reference):
    __module__ = __name__

    def addHook(self, tool, sobj=None, tobj=None):
        if not (tobj.hasRelationshipTo(sobj, self.relationship) or hasattr(tobj, '_v_addingReference')):
            sobj._v_addingReference = 1
            tool.addReference(tobj, sobj, self.relationship, referenceClass=BidirectionalReference)
            del sobj._v_addingReference

    def delHook(self, tool, sobj=None, tobj=None):
        if tobj.hasRelationshipTo(sobj, self.relationship) and not hasattr(tobj, '_v_deletingReference'):
            sobj._v_deletingReference = 1
            tool.deleteReference(tobj, sobj.UID(), self.relationship)
            del sobj._v_deletingReference


SymmetricalReference = BidirectionalReference
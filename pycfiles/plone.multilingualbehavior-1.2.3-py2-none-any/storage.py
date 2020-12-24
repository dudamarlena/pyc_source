# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/plone/multilingual/storage.py
# Compiled at: 2013-10-15 10:29:21
from zope.interface import implements
from BTrees.OOBTree import OOBTree
from OFS.SimpleItem import SimpleItem
from plone.multilingual.interfaces import IMultilingualStorage

class CanonicalStorage(SimpleItem):
    implements(IMultilingualStorage)
    id = 'portal_multilingual'

    def __init__(self):
        self.id = id
        self.canonicals = OOBTree()

    def get_canonical(self, id):
        """ get a canonical for a specific content-id """
        canonical = None
        if id in self.canonicals:
            canonical = self.canonicals[id]
        return canonical

    def add_canonical(self, id, canonical):
        """ add a canonical
            there is a usecase where the id can already exist on the OOBTree
        """
        if not self.canonicals.insert(id, canonical):
            canonical_old = self.get_canonical(id)
            if len(canonical_old.get_keys()) > 1:
                canonical_old.remove_item_by_id(id)
                self.remove_canonical(id)
            else:
                self.remove_canonical(id)
                del canonical_old
            self.canonicals.insert(id, canonical)

    def remove_canonical(self, id):
        """ remove a canonical """
        self.canonicals.pop(id)

    def get_canonicals(self):
        """ get all canonicals """
        return self.canonicals
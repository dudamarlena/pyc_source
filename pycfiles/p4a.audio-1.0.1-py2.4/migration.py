# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/audio/migration.py
# Compiled at: 2007-11-27 08:43:15
from zope import interface
from zope import component
from Products.CMFCore import utils as cmfutils
from OFS import interfaces as ofsifaces

class IMigratable(interface.Interface):
    """An interface for determining if something is migrateable"""
    __module__ = __name__

    def migrate():
        """Migrate the contextual object.
        """
        pass


class IMigrator(interface.Interface):
    __module__ = __name__

    def migrate(container, provides):
        """Search out all objects in a container and migrate them if
        possible.  The *provides* argument specifies the necessary
        interface an object must provide to even attempt migration.  This
        method should return the total number of objects migrated.
        """
        pass


class Migrator(object):
    __module__ = __name__
    interface.implements(IMigrator)

    def _attempt(self, container, obj):
        migratable = component.queryMultiAdapter((container, obj), IMigratable)
        if migratable is not None:
            if migratable.migrate():
                self.migrated += 1
        return

    def _walk(self, objmanager, provides):
        for obj in objmanager.objectValues():
            if provides.providedBy(obj):
                self._attempt(objmanager, obj)
            childobjmanager = ofsifaces.IObjectManager(obj, None)
            if childobjmanager is not None:
                self._walk(childobjmanager, provides)

        return

    def migrate(self, container, provides):
        self.migrated = 0
        objmanager = ofsifaces.IObjectManager(container)
        self._walk(objmanager, provides)
        return self.migrated
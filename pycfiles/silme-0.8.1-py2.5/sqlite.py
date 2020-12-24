# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/silme/io/sqlite.py
# Compiled at: 2010-06-12 17:55:55
import silme.io
from silme.io.clients import IOClient, DBClient
from silme.core import L10nPackage, L10nObject, EntityList, Object, Entity
import os
from pysqlite2 import dbapi2 as sqlite

def register(Manager):
    Manager.register(SQLiteClient)


class SQLiteClient(DBClient):
    name = 'sqlite'
    desc = 'SQLite reader/writer'
    type = IOClient.__name__

    @classmethod
    def matches_path(cls, path):
        """
        tests if the ioclient should be used for this type of path
        Matches any sqlite:
        """
        return path.startswith('sqlite:')

    @classmethod
    def get_entitylist(cls, path, source=False, code='default', parser=None):
        entityList = EntityList()
        (path, table) = cls._explode_path(path)
        con = cls._connected()
        if not con:
            cls._connect(path)
        cursor = cls.connection.cursor()
        cursor.execute('SELECT * FROM ' + table)
        for row in cursor:
            entitylist.add_entity(Entity(row[0], row[1]))

        cursor.close()
        if not con:
            cls._close()
        return entitylist

    @classmethod
    def get_l10npackage(cls, path, load_objects=True):
        l10npackage = L10nPackage()
        cls._connect(path)
        l10npackage.id = os.path.basename(path)
        l10npackage.objects['L10nTable'] = L10nObject(cls.build_entitylist(path, 'L10nTable'))
        cls._close()
        return l10npackage

    @classmethod
    def _explode_path(cls, path):
        return (
         path, 'l10n')

    @classmethod
    def _connect(cls, path):
        cls.connection = sqlite.connect(path)

    def _close(cls):
        if cls._connected():
            cls.connection.close()
            cls.connection = None
        return

    def _connected():
        return bool(cls.connection)
# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jld\backup\gliffy_db.py
# Compiled at: 2009-01-13 14:40:52
""" Gliffy DB class
    @author: Jean-Lou Dupont
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: gliffy_db.py 795 2009-01-13 19:42:53Z JeanLou.Dupont $'
import os, datetime
from sqlobject import *
import sqlite3 as sql, jld.api as api, jld.tools.db as db

class Diagrams(SQLObject):
    """ Gliffy diagrams database table
    """
    did = StringCol()
    etag = StringCol()
    added = DateTimeCol()
    exported = DateTimeCol()
    _attributesToVerify = [
     'did', 'exported', 'etag']

    @classmethod
    def getToExportList(cls):
        """ Returns a list of entries that aren't exported yet
        """
        return cls.select()

    @classmethod
    def getAll(cls):
        """ Returns all the entries
            @return: SQLObject list 
        """
        list = []
        all = cls.select(orderBy=DESC(cls.q.added))
        try:
            for one in all:
                entry = cls._formatOne(one)
                list.append(entry)

        except:
            pass

        return list

    @classmethod
    def _formatOne(cls, entry):
        """ Format an SQLObject result object (entry)
            to a dictionary object.
        """
        result = {}
        result['did'] = entry.did
        result['added'] = entry.added
        result['etag'] = entry.etag
        result['exported'] = entry.exported
        return result

    @classmethod
    def updateFromList(cls, list):
        """ Updates the database from the specified list.
            Used solely during the ''import'' command.
            
            @param list: the list of ids
            @return: tuple( total, updated, created )
        """
        total = len(list)
        updated = 0
        created = 0
        for did in list:
            dgs = cls.select(cls.q.did == did)
            try:
                diagram = dgs[0]
            except:
                diagram = None

            if diagram is None:
                entry = {'did': did}
                created = created + 1
                cls._createOne(entry)

        return (
         total, updated, created)

    @classmethod
    def _createOne(cls, entry):
        """ Creates one post entry
        """
        Diagrams(did=entry['did'], exported=None, etag=None, added=datetime.datetime.now())
        return

    @classmethod
    def _updateOne(cls, entry, diagram):
        """Processes one entry: verifies if the entry needs updating
            @param entry: the entry from Client API
            @param diagram:  the sqlobject
            
            @return: True if the entry needed updating
        """
        needsUpdate = False
        for att in cls._attributesToVerify:
            local = getattr(diagram, att)
            remote = entry[att]
            if local != remote:
                needsUpdate = True
                break

        if needsUpdate:
            diagram.set(did=entry['did'], etag=entry['etag'], added=entry['added'], exported=entry['exported'])
        return needsUpdate


class Db(db.BaseSQLObjectDb2):

    def __init__(self, filepath):
        db.BaseSQLObjectDb2.__init__(self, filepath)

    def initTable(self, connection):
        Diagrams._connection = connection
        Diagrams.createTable(ifNotExists=True)


if __name__ == '__main__':
    db = Db(':memory:')
# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Documents and Settings\Jean-Lou Dupont\My Documents\workspace_gae\jldupont\trunk\libs\python\jld\jld\backup\mindmeister_db.py
# Compiled at: 2008-12-16 20:03:04
""" MindMeister DB class
    @author: Jean-Lou Dupont
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: mindmeister_db.py 753 2008-12-17 01:03:03Z JeanLou.Dupont $'
import os, datetime
from sqlobject import *
import sqlite3 as sql, jld.api as api, jld.tools.date as tdate, jld.tools.mos as mos, jld.tools.db as db

class Maps(SQLObject):
    """ MindMeister Maps database
        Used to store map related information
    """
    mapid = StringCol()
    title = StringCol()
    created = DateTimeCol()
    modified = DateTimeCol()
    tags = StringCol()
    exported = DateTimeCol()
    _attributesToVerify = [
     'title', 'modified', 'tags']

    @classmethod
    def getToExportList(cls):
        """ Selects the maps for which 
            'exported' < 'modified' 
            ie: exported datime is older OR exported == None
        """
        return cls.select(OR(cls.q.modified != cls.q.exported, cls.q.exported == None))

    @classmethod
    def getExportList(cls):
        list = []
        all = cls.getToExportList()
        for one in all:
            entry = cls.formatOne(one)
            list.append(entry)

        return list

    @classmethod
    def getAll(cls):
        list = []
        all = cls.select()
        for one in all:
            entry = cls.formatOne(one)
            list.append(entry)

        return list

    @classmethod
    def formatOne(cls, entry):
        result = {}
        result['mapid'] = entry.mapid
        result['title'] = entry.title
        result['created'] = entry.created
        result['modified'] = entry.modified
        result['tags'] = entry.tags
        result['exported'] = entry.exported
        return result

    @classmethod
    def updateFromList(cls, list):
        """ Updates the database from the specified list
        """
        total = len(list)
        updated = 0
        created = 0
        for entry in list:
            id = entry['mapid']
            map = Maps.select(Maps.q.mapid == id)
            try:
                mid = map[0].mapid
            except:
                mid = None

            cls.formatEntry(entry)
            if mid is None:
                created = created + 1
                Maps(mapid=entry['mapid'], title=entry['title'], modified=entry['modified'], exported=entry.get('exported'), tags=entry['tags'], created=entry['created'])
            elif cls._processOne(entry, map[0]):
                updated = updated + 1

        return (
         total, updated, created)

    @classmethod
    def _processOne(cls, entry, map):
        """Processes one entry: verifies if the entry needs updating
            @param entry: the map entry
            @param map: the map sqlobject
            @return: True if the entry needed updating
        """
        updated = False
        for att in cls._attributesToVerify:
            local = getattr(map, att)
            remote = entry[att]
            if local != remote:
                updated = True
                break

        if updated:
            map.set(title=entry['title'], modified=entry['modified'], tags=entry['tags'], created=entry['created'])
        return updated

    @classmethod
    def formatEntry(cls, entry):
        """ Formats one entry
        """
        entry['modified'] = tdate.convertDate(entry['modified'])
        entry['created'] = tdate.convertDate(entry['created'])


class Db(db.BaseSQLObjectDb):
    """ Db class; used to bootstrap SQLObject 
    """

    def __init__(self, filepath):
        db.BaseSQLObjectDb.__init__(self, filepath)

    def initTable(self):
        Maps.createTable(ifNotExists=True)


if __name__ == '__main__':
    db = Db(':memory:')
    before = datetime.datetime(1971, 3, 31)
    now = datetime.datetime.now()
    after = datetime.datetime(2030, 3, 31)
    m1 = Maps(mapid='1', modified=now, tags='', exported=before, title='title', created=datetime.datetime.now())
    m2 = Maps(mapid='2', modified=now, tags='', exported=None, title='title', created=datetime.datetime.now())
    m3 = Maps(mapid='3', modified=now, tags='', exported=after, title='title', created=datetime.datetime.now())
    list = Maps.getToExportList()
    for item in list:
        print item

    print Maps.select(Maps.q.mapid == '4').count()
    m4 = Maps(mapid='4', modified=now, tags='', exported=None, title='title4', created=datetime.datetime.now())
    m4_ = Maps(mapid='4', modified=now, tags='', exported=None, title='title4_', created=datetime.datetime.now())
    print Maps.select(Maps.q.mapid == '4')[0].title
    print '####################'
    m5 = Maps(mapid='5', modified=now, tags='', exported=None, title='title5', created=datetime.datetime.now())
    m5.set(title='title5__')
    print Maps.select(Maps.q.mapid == '5')[0].title
    print Maps.select(Maps.q.mapid == '6').count()
    print '####################'
    d = {'mapid': '6', 'modified': now, 'tags': '', 'exported': None, 'title': 'map 6', 'created': now}
    m6 = Maps(d)
    print m6
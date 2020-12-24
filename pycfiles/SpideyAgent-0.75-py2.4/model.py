# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spider/model.py
# Compiled at: 2006-03-30 20:30:21
from sqlobject import *
from turbogears.database import AutoConnectHub
from sqlobject.mysql.mysqlconnection import MySQLConnection
import time, threading, MySQLdb
threadlocker = threading.Lock()
hub = AutoConnectHub()

def connect(threadIndex):
    """ Function to create a connection at the start of the thread """
    global hub
    hub.threadConnection = MySQLConnection('spiderpydb', 'root', 'sniggle', 'localhost', 3306)


class RootSite(SQLObject):
    __module__ = __name__
    _connection = hub
    address = StringCol()
    user = ForeignKey('User')


class Word(SQLObject):
    __module__ = __name__
    _connection = hub
    data = StringCol()
    entries = MultipleJoin('Entry')


class Entry(SQLObject):
    __module__ = __name__
    _connection = hub
    word = StringCol()
    uri = ForeignKey('URI')
    user = ForeignKey('User')


class URI(SQLObject):
    __module__ = __name__
    _connection = hub
    address = StringCol()
    data = StringCol()
    time = StringCol()


class Admin(SQLObject):
    __module__ = __name__
    _connection = hub
    password = StringCol()
    email = StringCol()


class User(SQLObject):
    __module__ = __name__
    _connection = hub
    name = StringCol()
    password = StringCol()
    email = StringCol()
    wait = StringCol()
    rootSites = MultipleJoin('RootSite')
    que = MultipleJoin('Que')


class Que(SQLObject):
    __module__ = __name__
    _connection = hub
    address = StringCol()
    time = FloatCol()
    user = ForeignKey('User')


def synch(func, *args):

    def wrapper(*args):
        try:
            threadlocker.acquire()
            return func(*args)
        finally:
            threadlocker.release()

    return wrapper


class ConnectionPool:
    __module__ = __name__

    def __init__(self, timeout=1, checkintervall=1):
        self.timeout = timeout
        self.lastaccess = {}
        self.connections = {}
        self.checkintervall = checkintervall
        self.lastchecked = time.time()
        self.lockingthread = None
        return

    def getConnection(self):
        tid = threading._get_ident()
        try:
            con = self.connections[tid]
        except KeyError:
            hub.threadConnection = MySQLConnection('spiderpydb', 'root', 'sniggle', 'localhost', 3306)
            con = hub.threadConnection
            print 'key error re-connecting'
            self.connections[tid] = con

        self.lastaccess[tid] = time.time()
        if self.lastchecked + self.checkintervall < time.time():
            self.cleanUp()
        return con

    def getLock(self):
        while not self._checklock():
            time.sleep(0.02)

        self.lockingthread = threading._get_ident()

    getLock = synch(getLock)

    def relLock(self):
        self.lockingthread = None
        return

    def _checklock(self):
        if self.lockingthread == threading._get_ident() or self.lockingthread is None:
            return True
        return False

    def cleanUp(self):
        dellist = []
        for con in self.connections:
            if self.lastaccess[con] + self.timeout < time.time():
                self.connections[con].close()
                del self.lastaccess[con]
                dellist.append(con)

        for l in dellist:
            del self.connections[l]
            print 'deleted connections'


conpool = ConnectionPool()
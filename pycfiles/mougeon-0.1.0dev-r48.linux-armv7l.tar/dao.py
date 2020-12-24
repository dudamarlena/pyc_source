# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/mougeon/core/persistence/dao.py
# Compiled at: 2012-03-08 09:55:34
"""
Created on Mar 5, 2012

@author: maemo
"""
import sqlite3
from threading import RLock
import os, os.path, logging
from mougeon.core.utils import *
from mougeon.common import version
version.getInstance().submitRevision('$Revision: 11 $')
DATABASE_URL = None

def checkStorage():
    """
    Test if the databse existe if not create a new one
    """
    if not os.path.isfile(DATABASE_URL):
        initStorage(DATABASE_URL)


def initStorage(dburl):
    """
    This function should be used to ensure the backend storage is available 
    """
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.executescript('\n        %s;        \n        ' % (TrackedCellTower.create_sql(),))
    conn.commit()
    c.close()


def getConnection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn


def releaseConnection(cnx):
    cnx.close()


def with_transaction_required(commit):
    """
    Decorator to handle local transaction.
    If none cnx arguments keywork is passed to the decorated function
    then this decorator create a new connexion.
    if the commit decorator argument is True, then if a local transaction where created
    then commit the local transaction.
    A the end, release the local connextion if any.
    """

    def wrap(f):

        def wrapped(*args, **kwargs):
            if kwargs['cnx'] is None:
                cnx = getConnection()
                kwargs['cnx'] = cnx
                local = True
            else:
                local = False
            try:
                return f(*args, **kwargs)
            finally:
                if local:
                    if commit:
                        cnx.commit()
                        releaseConnection(cnx)

            return

        return wrapped

    return wrap


class ICrud:
    """
    CRUD interface
    """

    def select(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def create(self):
        raise NotImplementedError

    def delete(selfself):
        raise NotImplementedError


class TrackedCellTower(ICrud):
    """
    A cell tower where the device has been registered
    """
    cellId = None
    opId = None
    country = None
    timestamp = None
    TABLE_NAME = 'track_cell_tower'

    @classmethod
    def create_sql(cls):
        return '\n            create table %s\n                (cellId text,\n                 opId text,\n                 country text,\n                 datetime text)\n            ' % (TrackedCellTower.TABLE_NAME,)

    def select(self):
        pass

    def update(self):
        pass

    @with_transaction_required(True)
    def create(self, cnx=None):
        cursor = cnx.cursor()
        cursor.execute('insert into %s values(?,?,?,?)' % self.TABLE_NAME, (self.cellId, self.opId, self.country, self.timestamp))
        cursor.close()

    @with_transaction_required(True)
    def delete(self, cnx=None):
        pass

    @classmethod
    @with_transaction_required(True)
    def clear(self, cnx=None):
        cursor = cnx.cursor()
        cursor.execute('DELETE FROM %s ' % self.TABLE_NAME)
        cursor.close()

    @classmethod
    @with_transaction_required(False)
    def free_mobile_record(self, cnx=None):
        resu = 0
        cursor = cnx.cursor()
        for free_op_code in FREE_MOBILE_OP_CODE:
            cursor.execute('select count() from %s where opId=? and country=?' % self.TABLE_NAME, (free_op_code, FREE_MOBILE_COUNTRY[0]))
            for count in cursor:
                logging.info('found Free Mobile record %s' % count[0])
                resu = resu + int(count[0])

        cursor.close()
        return resu

    @classmethod
    @with_transaction_required(False)
    def orange_record(self, cnx=None):
        resu = 0
        cursor = cnx.cursor()
        for orange_op_code in ORANGE_OP_CODE:
            cursor.execute('select count() from %s where opId=? and country=?' % self.TABLE_NAME, (orange_op_code, ORANGE_COUNTRY[0]))
            for count in cursor:
                logging.info('Found Orange record %s' % count[0])
                resu = resu + int(count[0])

        cursor.close()
        return resu

    @classmethod
    @with_transaction_required(False)
    def total_record(self, cnx=None):
        resu = 0
        cursor = cnx.cursor()
        cursor.execute('select count() from %s ' % self.TABLE_NAME)
        for count in cursor:
            logging.info('Found Total record %s' % count[0])
            resu = resu + int(count[0])

        cursor.close()
        return resu
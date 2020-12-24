# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\db\cnx.py
# Compiled at: 2013-02-02 01:41:44
"""This module handles the conection to the database"""
from __future__ import absolute_import, unicode_literals, print_function
import contextlib, ZODB.DB, ZODB.FileStorage, transaction
doc = b'PersistentList are not lazy , so be carefull.\nis better to use IOBTree s when possible (or OOBTrees)\nChoosing the "key" carefully can be a big optimization\nie using a timestamp as a key for the bills will allow to search by date much more easily as only the keys are loaded, and can be\ncropped by date with BTree.values(min=someminddata, max=somemaxdate)\n(thansk kosh @ #zodb @irc.freenode.net)\n'

class MiZODB(object):

    def __init__(self, file_name=b'd', server=None, port=8090):
        """Handles a ZODB connection"""
        from banta.db import updates as _up
        if server:
            import ZEO.ClientStorage
            try:
                self.storage = ZEO.ClientStorage.ClientStorage((server, port), blob_dir=b'./blobs')
            except:
                self.storage = ZEO.ClientStorage.ClientStorage((server, port))

        else:
            try:
                self.storage = ZODB.FileStorage.FileStorage(file_name, blob_dir=b'./blobs')
            except:
                self.storage = ZODB.FileStorage.FileStorage(file_name)

        self.db = ZODB.DB(self.storage)
        self.cnx = self.db.open()
        self.root = self.cnx.root()
        _up.init(self)
        self.products = self.root.get(b'products')
        self.typePays = self.root.get(b'typePays')
        self.clients = self.root.get(b'clients')
        self.bills = self.root.get(b'bills')
        self.printer = self.root.get(b'printer')
        self.providers = self.root.get(b'providers')
        self.users = self.root.get(b'users')
        self.moves = self.root.get(b'moves')
        self.categories = self.root.get(b'categories')
        self.buys = self.root.get(b'buys')
        self.limits = self.root.get(b'limits')
        self.type_tax = self.root.get(b'typeTax')

    def commit(self, user=None, note=None):
        """Esta funcion permite realizar un commit 
                recibe como parametros el nombre de usuario y una nota
                las que se guardan con el commit y se informan en el log"""
        trans = transaction.get()
        if user:
            trans.setUser(user)
        if note:
            trans.note(note)
        trans.commit()

    def abort(self):
        trans = transaction.get()
        trans.abort()

    def close(self):
        self.cnx.close()
        self.db.close()
        self.storage.close()

    @contextlib.contextmanager
    def threaded(self):
        """
                A context manager for connections outside the main thread
                This is meant to be used on functions that need to use the database from another thread
                ensures that the transaction will always be commited, or aborted in case of an exception.

                use like:

                with banta.db.DB.threaded() as root:
                        if 'something' in root['products']:
                                raise ....

                if an exception occurs inside the "with", the transaction will get aborted
                else, the transaction gets commited.
                a new connection has its own root object.
                in theory you can use another connection in another thread to allow a better threading usability

                the returning object is a new root object.
                """
        cnx = self.db.open()
        root = cnx.root()
        try:
            yield root
            self.commit()
        except Exception as e:
            self.abort()
            cnx.close()
            raise e

        cnx.close()
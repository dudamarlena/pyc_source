# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange_django/db_drivers.py
# Compiled at: 2011-05-12 16:13:19
from django.db import transaction
from linkexchange.db_drivers import BaseMultiHashDriver
from linkexchange_django.models import DBHash, DBHashItem

class DjangoMultiHashDriver(BaseMultiHashDriver):
    """
    Django ORM multihash driver.
    """

    def __init__(self, dbname):
        self.dbname = dbname

    def load(self, hashkey):
        try:
            return DBHash.objects.get(dbname=self.dbname, key=hashkey)
        except DBHash.DoesNotExist:
            raise KeyError(hashkey)

    def get_mtime(self, hashkey):
        try:
            return DBHash.objects.get(dbname=self.dbname, key=hashkey).mtime
        except DBHash.DoesNotExist:
            raise KeyError(hashkey)

    def _run_in_transaction(self, func, args=[], kwargs={}):
        ok = False
        sid = transaction.savepoint()
        try:
            result = func(*args, **kwargs)
            ok = True
        finally:
            if ok:
                transaction.savepoint_commit(sid)
            else:
                transaction.savepoint_rollback(sid)

        return result

    def _get_hash(self, hashkey):
        try:
            return DBHash.objects.get(dbname=self.dbname, key=hashkey)
        except DBHash.DoesNotExist:
            pass

        h = DBHash(dbname=self.dbname, key=hashkey)
        h.save()
        return h

    def save(self, hashkey, newhash, blocking=True):

        def _save():
            h = self._get_hash(hashkey)
            h.set_items(newhash)
            h.save()
            return True

        return self._run_in_transaction(_save)

    def modify(self, hashkey, otherhash, blocking=True):

        def _modify():
            h = self._get_hash(hashkey)
            h.update_items(otherhash)
            h.save()
            return True

        return self._run_in_transaction(_modify)

    def delete(self, hashkey, keys, blocking=True):

        def _delete():
            h = self._get_hash(hashkey)
            h.delete_items(keys)
            h.save()
            return True

        return self._run_in_transaction(_delete)
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/lockmanager.py
# Compiled at: 2012-10-12 07:02:39
import uuid, json
from datetime import datetime
from coils.foundation import Lock
from sqlalchemy import *

class LockManager(object):
    __slots__ = '_ctx'

    def __init__(self, ctx):
        self._ctx = ctx

    def _now(self):
        return int(datetime.utcnow().strftime('%s'))

    def locks_on(self, entity, all_locks=False, delete=False, write=True, run=False, exclusive=True):
        """
        Returns all the locks on the specified entity with the described application(s).
        
        :param entity: entity to check for locks
        :param all_locks: if set locks will be returned regardless of application.
        :param delete: limit locks to those with a delete application
        :param write: limit locks to those with a write application
        :param run: limit locks to those with a run application
        :param exclusive: limit locks to exclusive locks
        """
        db = self._ctx.db_session()
        t = self._now()
        clause = and_(Lock.object_id == entity.object_id, Lock.granted <= t, Lock.expires >= t)
        if not all_locks:
            if exclusive:
                clause.append(Lock.exclusive == 'Y')
            if run:
                clause.append(Lock.operations.like('%r%'))
            if write:
                clause.append(Lock.operations.like('%w%'))
            if delete:
                clause.append(Lock.operations.like('%d%'))
        query = db.query(Lock).filter(clause)
        return query.all()

    def can_upgrade(self, mylock, alllocks, delete, write, run, exclusive):
        if mylock.is_exclusive:
            return True
        if delete == mylock.delete and write == mylock.write and run == mylock.run and exclusive == mylock.is_exclusive:
            return True
        locks = [ x for x in alllocks if x != mylock ]
        for otherlock in locks:
            if otherlock.is_exclusive and other.owner_id != self._ctx.account_id:
                return False
            if otherlock.run and mylock.run:
                return False
            if otherlock.write and mylock.write:
                return False
            if otherlock.delete and mylock.delete:
                return False

        return True

    def lock(self, entity, duration, data, delete=False, write=True, run=False, exclusive=True):
        """
        Apply, upgrade, or resh a lock on the entity for a given application. By default if no
        application is specified the lock will be write+exclusive.
        
        :param entity:
        :param duration:
        :param data:
        :param delete:
        :param write:
        :param run:
        :param exclusive:
        """
        db = self._ctx.db_session()
        my_lock = None
        locks = self.locks_on(entity, all_locks=True)
        for lock in locks:
            if lock.owner_id != self._ctx.account_id and lock.exclusive:
                return (False, lock)
            elif lock.owner_id == self._ctx.account_id:
                my_lock = lock

        if my_lock:
            if self.can_upgrade(my_lock, locks, delete=delete, write=write, run=run, exclusive=exclusive):
                self.refresh(token=my_lock.token, duration=duration, data=data)
                my_lock.update_mode(delete=delete, write=write, run=run, exclusive=exclusive)
                return (
                 True, my_lock)
            else:
                return (
                 False, None)
        else:
            my_lock = Lock(owner_id=self._ctx.account_id, object_id=entity.object_id, duration=duration, data=data, delete=delete, write=write, run=run, exclusive=exclusive)
            self._ctx.db_session().add(my_lock)
        return (
         True, my_lock)

    def refresh(self, token, duration, data=None):
        """
        Refresh the specified lock for an addition period of time. The application
        of the lock is not changed. If the lock referred to is not found or has 
        expired a None is returned; if the lock is refreshed the Lock entity is
        returned.
        
        :param token:
        :param duration:
        :param data:
        """
        t = self._now()
        db = self._ctx.db_session()
        query = db.query(Lock).filter(and_(Lock.token == token, Lock.owner_id == self._ctx.account_id, Lock.granted <= t, Lock.expires >= t))
        data = query.all()
        if data:
            my_lock = data[0]
            my_lock.expires = self._now() + duration
            return my_lock
        else:
            return

    def unlock(self, entity, token=None):
        """
        Remove all the locks on a specified entity or the specified
        lock [via token] on the specified entity.  If token is specified it
        must be a lock on the references entity.
        
        :param entity: The entity on which the lock or locks should be removed.
        :param token: The token of an individual lock to be removed.
        """
        db = self._ctx.db_session()
        if token:
            query = db.query(Lock).filter(and_(Lock.object_id == entity.object_id, Lock.owner_id == self._ctx.account_id, Lock.token == token))
        else:
            query = db.query(Lock).filter(and_(Lock.object_id == entity.object_id, Lock.owner_id == self._ctx.account_id))
        locks = query.all()
        if locks:
            for lock in locks:
                self._ctx.db_session().delete(lock)

            return True
        return False

    def get_lock(self, token):
        """
        Retrieve the lock entity with the specified token. If the token does not
        reference a current lock None will be returned.
        
        :param token: The lock token (string)
        """
        t = self._now()
        db = self._ctx.db_session()
        query = db.query(Lock).filter(and_(Lock.token == token, Lock.granted <= t, Lock.expires >= t))
        data = query.all()
        if data:
            return data[0]
        else:
            return

    def is_locked(self, entity, delete=False, write=False, run=False, exclusive=False):
        """
        Return True of False indicating if any locks of the specified application
        are applied to the entity.
        
        :param entity:
        :param delete:
        :param write:
        :param run:
        :param exclusive:
        """
        locks = self.locks_on(entity, delete=delete, write=write, run=run, exclusive=exclusive)
        if locks:
            return True
        return False

    def have_lock(self, entity, run=False, delete=False, write=False, exclusive=False):
        """
        Return True or False indicating if the current context has a lock of the specified 
        application.
        
        :param entity:
        :param run:
        :param delete:
        :param write:
        :param exclusive:
        """
        locks = self.locks_on(entity, delete=delete, write=write, run=run, exclusive=exclusive)
        return bool([ lock for lock in locks if lock.owner_id == self._ctx.account_id ])
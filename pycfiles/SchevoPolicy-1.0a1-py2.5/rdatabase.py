# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/schevopolicy/rdatabase.py
# Compiled at: 2008-01-19 12:32:25
"""Restricted database class.

For copyright, license, and warranty, see bottom of file.
"""
import sys
from schevo.lib import optimize
from schevo import base
from schevo.entity import Entity
from schevo.label import label, with_label
from schevopolicy.convert import unrestricted_args
from schevopolicy.error import ContextMismatch
from schevopolicy.rentity import RestrictedEntity
from schevopolicy.rextent import RestrictedExtent
from schevopolicy.rtransaction import RestrictedTransaction

class RestrictedDatabase(base.Database):

    def __init__(self, policy, context):
        policy.attach(self, context)
        db = policy.db
        self._db = db
        self.label = label(db)
        rextents = self._rextents = {}
        for extent in policy.db.extents():
            name = extent.name
            rextent = RestrictedExtent(policy, context, self, extent)
            rextents[name] = rextent
            rextents[extent] = rextent
            rextents[extent.id] = rextent
            setattr(self, name, rextent)

        self.t = RestrictedDatabaseTransactions(policy, context, self)

    def close(self):
        return self._db.close()

    def execute(self, *transactions, **kw):
        if not self._allow():
            self._unauthorized()
        policy = self._policy
        context = self._context
        to_execute = []
        for tx in transactions:
            if not isinstance(tx, RestrictedTransaction):
                raise ContextMismatch('Transaction %r is unrestricted.' % tx)
            if tx._policy is not policy:
                raise ContextMismatch('Transaction %r is from the wrong policy.' % tx)
            if tx._context != context:
                raise ContextMismatch('Transaction %r is from the wrong context.' % tx)
            to_execute.append(tx._tx)

        result = self._db.execute(*to_execute, **kw)
        if isinstance(result, Entity):
            result = RestrictedEntity(policy, context, self, self._rextents[result._extent], result)
        elif isinstance(result, (list, tuple)):
            old_result = result
            result = []
            for inner in old_result:
                if isinstance(inner, Entity):
                    inner = RestrictedEntity(policy, context, self, self._rextents[inner._extent], inner)
                result.append(inner)

            result = type(old_result)(result)
        return result

    def extent(self, name):
        if not self._allow():
            self._unauthorized()
        return self._rextents[name]

    def extents(self):
        if not self._allow():
            self._unauthorized()
        rextents = self._rextents
        return [ rextents[name] for name in self.extent_names() ]

    def extent_names(self):
        if not self._allow():
            self._unauthorized()
        return self._db.extent_names()

    def _icon(self, name):
        return self._db._icon(name)

    def populate(self, sample_name=''):
        if not self._allow():
            self._unauthorized()
        return self._db.populate(sample_name)

    @property
    def schema(self):
        return self._db.schema


class RestrictedDatabaseTransactions(object):

    def __init__(self, policy, context, rdb):
        policy.attach(self, context)
        self._db = rdb
        self._t = rdb._db.t

    def __getattr__(self, name):
        if not self._allow():
            self._unauthorized()
        method = getattr(self._t, name)
        policy = self._policy
        context = self._context

        @with_label(label(method))
        def tx_method(*args, **kw):
            (args, kw) = unrestricted_args(args, kw)
            tx = method(*args, **kw)
            return RestrictedTransaction(policy, context, self._db, tx)

        tx_method.__name__ = method.__name__
        return tx_method

    def __iter__(self):
        allow_t = self._allow_t
        return iter((name for name in self._t if allow_t(None, None, name)))


optimize.bind_all(sys.modules[__name__])
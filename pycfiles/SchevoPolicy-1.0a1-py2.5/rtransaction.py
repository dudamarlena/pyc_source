# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/schevopolicy/rtransaction.py
# Compiled at: 2008-01-19 12:32:25
"""Restricted transaction class.

For copyright, license, and warranty, see bottom of file.
"""
import sys
from schevo.lib import optimize
from schevo import base
from schevo.entity import Entity
from schevo.label import label
from schevopolicy.rentity import RestrictedEntity

class RestrictedTransaction(base.Transaction):

    def __init__(self, policy, context, rdb, transaction):
        policy.attach(self, context)
        d = self.__dict__
        d.update(dict(_db=rdb, _tx=transaction, _field_spec=transaction._field_spec, _inversions=transaction._inversions, _label=label(transaction), sys=transaction.sys, x=transaction.x))
        d['f'] = RestrictedTransactionFields(policy, context, self)

    def __getattr__(self, name):
        if not self._allow():
            self._unauthorized()
        if name not in self._field_spec:
            raise AttributeError('Field %r not in %r' % (name, self))
        value = getattr(self._tx, name)
        if isinstance(value, Entity):
            db = self._db
            rextent = db.extent(value._extent)
            value = RestrictedEntity(self._policy, self._context, db, rextent, value)
        return value

    def __repr__(self):
        return '<restricted %r>' % self._tx

    def __setattr__(self, name, value):
        if not self._allow():
            self._unauthorized()
        tx = self._tx
        if name in self._field_spec:
            if isinstance(value, RestrictedEntity):
                value = value._entity
            return setattr(tx, name, value)
        else:
            return setattr(self, name, value)

    @property
    def _changes(self):
        return self._tx._changes

    @property
    def _executed(self):
        return self._tx._executed

    @property
    def _label(self):
        return label(self._tx)

    def _undo(self):
        tx = self._tx._undo()
        if tx is None:
            return
        else:
            return RestrictedTransaction(self._policy, self._context, self._db, tx)
        return


class RestrictedTransactionFields(object):

    def __init__(self, policy, context, rtx):
        policy.attach(self, context)
        self._db = rtx._db
        self._f = rtx._tx.f

    def __delattr__(self, name):
        delattr(self._f, name)

    def __getattr__(self, name):
        f = self._f
        field = getattr(f, name)
        if field.may_store_entities:
            field = field.copy()
            db = self._db
            policy = self._policy
            context = self._context
            extent = db.extent

            def to_rentity(e):
                return RestrictedEntity(policy, context, db, extent(e._extent), e)

            field._transform(to_rentity)
        return field

    def __iter__(self):
        return iter(self._f)


optimize.bind_all(sys.modules[__name__])
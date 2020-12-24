# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/schevopolicy/rentity.py
# Compiled at: 2008-01-19 12:32:25
"""Restricted entity class.

For copyright, license, and warranty, see bottom of file.
"""
import sys
from schevo.lib import optimize
from schevo import base
from schevo.entity import Entity
from schevo import field
from schevo.label import label, with_label

class RestrictedEntity(base.Entity):

    def __init__(self, policy, context, rdb, rextent, entity):
        policy.attach(self, context)
        self._db = rdb
        self._extent = rextent
        self._entity = entity
        self._field_spec = entity._field_spec
        self._oid = entity._oid
        self.f = RestrictedEntityFields(policy, context, self)
        self.m = RestrictedEntityOneToMany(policy, context, self)
        self.sys = RestrictedEntitySys(policy, context, self)
        self.t = RestrictedEntityTransactions(policy, context, self)
        self.v = RestrictedEntityViews(policy, context, self)

    def _unauthorized_if_getattr_disallowed(self):
        if not self._allow_v(self._entity, None) or not self._allow():
            self._unauthorized()
        return

    def __cmp__(self, other):
        if isinstance(other, RestrictedEntity):
            other = other._entity
        return cmp(self._entity, other)

    def __eq__(self, other):
        if isinstance(other, RestrictedEntity):
            return self._entity == other._entity
        else:
            return self._entity == other

    def __getattr__(self, name):
        if name not in self._field_spec:
            raise AttributeError('Field %r not in %r' % (name, self))
        self._unauthorized_if_getattr_disallowed()
        f = self._entity.f[name]
        if f.may_store_entities:
            f = f.copy()
            db = self._db
            policy = self._policy
            context = self._context
            extent = db.extent

            def to_rentity(e):
                return RestrictedEntity(policy, context, db, extent(e._extent), e)

            f._transform(to_rentity)
        return f.get()

    def __hash__(self):
        return hash(self._entity)

    @property
    def _default_key(self):
        return self._entity._default_key

    @property
    def _label(self):
        return label(self._entity)

    def __repr__(self):
        return '<restricted %r>' % self._entity

    def __str__(self):
        return str(self._entity)

    def __unicode__(self):
        return unicode(self._entity)


class RestrictedEntityFields(object):

    def __init__(self, policy, context, rentity):
        policy.attach(self, context)
        self._db = rentity._db
        self._entity = rentity._entity

    def __getattr__(self, name):
        entity = self._entity
        if not self._allow_v(entity, name) or not self._allow():
            self._unauthorized()
        field = getattr(entity.f, name)
        if field.may_store_entities:
            field = field.copy()
            db = self._db

            def to_rentity(e):
                return RestrictedEntity(self._policy, self._context, db, db.extent(e._extent), e)

            field._transform(to_rentity)
        return field

    def __iter__(self):
        return iter(self._entity.f)


class RestrictedEntityOneToMany(object):

    def __init__(self, policy, context, rentity):
        policy.attach(self, context)
        self._db = rentity._db
        self._m = rentity._entity.m

    def __getattr__(self, name):
        db = self._db
        orig = self._m[name]

        def wrapped(*args, **kw):
            return [ RestrictedEntity(self._policy, self._context, db, db.extent(e._extent), e) for e in orig(*args, **kw)
                   ]

        return wrapped

    def __iter__(self):
        return iter(self._m)


class RestrictedEntitySys(object):

    def __init__(self, policy, context, rentity):
        policy.attach(self, context)
        self._db = rentity._db
        self._entity = entity = rentity._entity
        self._sys = entity.sys

    @property
    def db(self):
        return self._db

    def count(self, other_extent_name=None, other_field_name=None):
        return self._entity.sys.count(other_extent_name, other_field_name)

    @property
    def extent(self):
        from schevopolicy.rextent import RestrictedExtent
        return RestrictedExtent(self._policy, self._context, self._db, self._sys.extent)

    def field_map(self, *filters):
        map = self._sys.field_map(*filters)
        new_map = type(map)()
        db = self._db
        p = self._policy
        c = self._context
        extent = db.extent
        for (field_name, field) in map.iteritems():
            if field.may_store_entities:
                field = field.copy()

                def to_rentity(e):
                    return RestrictedEntity(p, c, db, extent(e._extent), e)

                field._transform(to_rentity)
            new_map[field_name] = field

        return new_map

    def _links_convert_link_structure(self, structure):
        db = self._db
        policy = self._policy
        context = self._context
        rextent = db.extent
        if isinstance(structure, dict):
            links = {}
            for ((e_name, f_name), others) in structure.iteritems():
                links[(e_name, f_name)] = [ RestrictedEntity(policy, context, db, rextent(e._extent), e) for e in others
                                          ]

            return links
        elif isinstance(structure, list):
            return [ RestrictedEntity(policy, context, db, rextent(e._extent), e) for e in structure
                   ]

    def links(self, other_extent_name=None, other_field_name=None):
        return self._links_convert_link_structure(self._entity.sys.links(other_extent_name, other_field_name))

    def links_filter(self, other_extent_name=None, other_field_name=None):
        orig_filter = self._entity.sys.links_filter(other_extent_name, other_field_name)

        def _filter():
            return self._links_convert_link_structure(orig_filter())

        return _filter

    @property
    def oid(self):
        return self._sys.oid

    @property
    def rev(self):
        return self._sys.rev


class RestrictedEntityTransactions(object):

    def __init__(self, policy, context, rentity):
        policy.attach(self, context)
        self._db = rentity._db
        self._entity = rentity._entity

    def __getattr__(self, name):
        entity = self._entity
        if not self._allow_t(entity._extent, entity, name) or not self._allow():
            self._unauthorized()
        method = getattr(entity.t, name)
        policy = self._policy
        context = self._context
        from schevopolicy.convert import unrestricted_args

        @with_label(label(method))
        def tx_method(*args, **kw):
            (args, kw) = unrestricted_args(args, kw)
            tx = method(*args, **kw)
            from schevopolicy.rtransaction import RestrictedTransaction
            return RestrictedTransaction(policy, context, self._db, tx)

        tx_method.__name__ = method.__name__
        return tx_method

    def __iter__(self):
        allow_t = self._allow_t
        entity = self._entity
        return iter((name for name in entity.t if allow_t(entity._extent, entity, name)))


class RestrictedEntityViews(object):

    def __init__(self, policy, context, rentity):
        policy.attach(self, context)
        self._entity = rentity._entity

    def __getattr__(self, name):
        entity = self._entity
        if not self._allow_v(entity, name) or not self._allow():
            self._unauthorized()
        method = getattr(entity.v, name)
        policy = self._policy
        context = self._context

        @with_label(label(method))
        def view_method(*args, **kw):
            view = method()
            return view

        view_method.__name__ = method.__name__
        return view_method

    def __iter__(self):
        allow_v = self._allow_v
        entity = self._entity
        return iter((name for name in entity.v if allow_v(entity, name)))


optimize.bind_all(sys.modules[__name__])
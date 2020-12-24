# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/db/models/query_utils.py
# Compiled at: 2018-07-11 18:15:30
"""
Various data structures used in query construction.

Factored out from django.db.models.query to avoid making the main module very
large and/or so that they can be used by other modules without getting into
circular import difficulties.
"""
from __future__ import unicode_literals
from django.db.backends import util
from django.utils import six
from django.utils import tree

class InvalidQuery(Exception):
    """
    The query passed to raw isn't a safe query to use with raw.
    """
    pass


class QueryWrapper(object):
    """
    A type that indicates the contents are an SQL fragment and the associate
    parameters. Can be used to pass opaque data to a where-clause, for example.
    """

    def __init__(self, sql, params):
        self.data = (
         sql, params)

    def as_sql(self, qn=None, connection=None):
        return self.data


class Q(tree.Node):
    """
    Encapsulates filters as objects that can then be combined logically (using
    & and |).
    """
    AND = b'AND'
    OR = b'OR'
    default = AND

    def __init__(self, *args, **kwargs):
        super(Q, self).__init__(children=list(args) + list(six.iteritems(kwargs)))

    def _combine(self, other, conn):
        if not isinstance(other, Q):
            raise TypeError(other)
        obj = type(self)()
        obj.add(self, conn)
        obj.add(other, conn)
        return obj

    def __or__(self, other):
        return self._combine(other, self.OR)

    def __and__(self, other):
        return self._combine(other, self.AND)

    def __invert__(self):
        obj = type(self)()
        obj.add(self, self.AND)
        obj.negate()
        return obj


class DeferredAttribute(object):
    """
    A wrapper for a deferred-loading field. When the value is read from this
    object the first time, the query is executed.
    """

    def __init__(self, field_name, model):
        self.field_name = field_name

    def __get__(self, instance, owner):
        """
        Retrieves and caches the value from the datastore on the first lookup.
        Returns the cached value.
        """
        from django.db.models.fields import FieldDoesNotExist
        non_deferred_model = instance._meta.proxy_for_model
        opts = non_deferred_model._meta
        assert instance is not None
        data = instance.__dict__
        if data.get(self.field_name, self) is self:
            try:
                f = opts.get_field_by_name(self.field_name)[0]
            except FieldDoesNotExist:
                f = [ f for f in opts.fields if f.attname == self.field_name
                    ][0]

            name = f.name
            val = self._check_parent_chain(instance, name)
            if val is None:
                val = getattr(non_deferred_model._base_manager.only(name).using(instance._state.db).get(pk=instance.pk), self.field_name)
            data[self.field_name] = val
        return data[self.field_name]

    def __set__(self, instance, value):
        """
        Deferred loading attributes can be set normally (which means there will
        never be a database lookup involved.
        """
        instance.__dict__[self.field_name] = value

    def _check_parent_chain(self, instance, name):
        """
        Check if the field value can be fetched from a parent field already
        loaded in the instance. This can be done if the to-be fetched
        field is a primary key field.
        """
        opts = instance._meta
        f = opts.get_field_by_name(name)[0]
        link_field = opts.get_ancestor_link(f.model)
        if f.primary_key and f != link_field:
            return getattr(instance, link_field.attname)
        else:
            return


def select_related_descend(field, restricted, requested, load_fields, reverse=False):
    """
    Returns True if this field should be used to descend deeper for
    select_related() purposes. Used by both the query construction code
    (sql.query.fill_related_selections()) and the model instance creation code
    (query.get_klass_info()).

    Arguments:
     * field - the field to be checked
     * restricted - a boolean field, indicating if the field list has been
       manually restricted using a requested clause)
     * requested - The select_related() dictionary.
     * load_fields - the set of fields to be loaded on this model
     * reverse - boolean, True if we are checking a reverse select related
    """
    if not field.rel:
        return False
    if field.rel.parent_link and not reverse:
        return False
    if restricted:
        if reverse and field.related_query_name() not in requested:
            return False
        if not reverse and field.name not in requested:
            return False
    if not restricted and field.null:
        return False
    if load_fields:
        if field.name not in load_fields:
            if restricted and field.name in requested:
                raise InvalidQuery(b'Field %s.%s cannot be both deferred and traversed using select_related at the same time.' % (
                 field.model._meta.object_name, field.name))
            return False
    return True


def deferred_class_factory(model, attrs):
    """
    Returns a class object that is a copy of "model" with the specified "attrs"
    being replaced with DeferredAttribute objects. The "pk_value" ties the
    deferred attributes to a particular instance of the model.
    """

    class Meta:
        proxy = True
        app_label = model._meta.app_label

    name = b'%s_Deferred_%s' % (model.__name__, (b'_').join(sorted(list(attrs))))
    name = util.truncate_name(name, 80, 32)
    overrides = dict([ (attr, DeferredAttribute(attr, model)) for attr in attrs
                     ])
    overrides[b'Meta'] = Meta
    overrides[b'__module__'] = model.__module__
    overrides[b'_deferred'] = True
    return type(str(name), (model,), overrides)


deferred_class_factory.__safe_for_unpickling__ = True
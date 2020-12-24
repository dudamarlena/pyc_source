# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/db/models/query_utils.py
# Compiled at: 2019-02-14 00:35:17
"""
Various data structures used in query construction.

Factored out from django.db.models.query to avoid making the main module very
large and/or so that they can be used by other modules without getting into
circular import difficulties.
"""
from __future__ import unicode_literals
import inspect
from collections import namedtuple
from django.db.models.constants import LOOKUP_SEP
from django.utils import tree
from django.utils.lru_cache import lru_cache
PathInfo = namedtuple(b'PathInfo', b'from_opts to_opts target_fields join_field m2m direct')

class InvalidQuery(Exception):
    """
    The query passed to raw isn't a safe query to use with raw.
    """
    pass


def subclasses(cls):
    yield cls
    for subclass in cls.__subclasses__():
        for item in subclasses(subclass):
            yield item


class QueryWrapper(object):
    """
    A type that indicates the contents are an SQL fragment and the associate
    parameters. Can be used to pass opaque data to a where-clause, for example.
    """
    contains_aggregate = False

    def __init__(self, sql, params):
        self.data = (
         sql, list(params))

    def as_sql(self, compiler=None, connection=None):
        return self.data


class Q(tree.Node):
    """
    Encapsulates filters as objects that can then be combined logically (using
    `&` and `|`).
    """
    AND = b'AND'
    OR = b'OR'
    default = AND

    def __init__(self, *args, **kwargs):
        super(Q, self).__init__(children=list(args) + list(kwargs.items()))

    def _combine(self, other, conn):
        if not isinstance(other, Q):
            raise TypeError(other)
        obj = type(self)()
        obj.connector = conn
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

    def resolve_expression(self, query=None, allow_joins=True, reuse=None, summarize=False, for_save=False):
        clause, joins = query._add_q(self, reuse, allow_joins=allow_joins, split_subq=False)
        query.promote_joins(joins)
        return clause


class DeferredAttribute(object):
    """
    A wrapper for a deferred-loading field. When the value is read from this
    object the first time, the query is executed.
    """

    def __init__(self, field_name, model):
        self.field_name = field_name

    def __get__(self, instance, cls=None):
        """
        Retrieves and caches the value from the datastore on the first lookup.
        Returns the cached value.
        """
        if instance is None:
            return self
        else:
            data = instance.__dict__
            if data.get(self.field_name, self) is self:
                val = self._check_parent_chain(instance, self.field_name)
                if val is None:
                    instance.refresh_from_db(fields=[self.field_name])
                    val = getattr(instance, self.field_name)
                data[self.field_name] = val
            return data[self.field_name]

    def _check_parent_chain(self, instance, name):
        """
        Check if the field value can be fetched from a parent field already
        loaded in the instance. This can be done if the to-be fetched
        field is a primary key field.
        """
        opts = instance._meta
        f = opts.get_field(name)
        link_field = opts.get_ancestor_link(f.model)
        if f.primary_key and f != link_field:
            return getattr(instance, link_field.attname)
        else:
            return


class RegisterLookupMixin(object):

    @classmethod
    def _get_lookup(cls, lookup_name):
        return cls.get_lookups().get(lookup_name, None)

    @classmethod
    @lru_cache(maxsize=None)
    def get_lookups(cls):
        class_lookups = [ parent.__dict__.get(b'class_lookups', {}) for parent in inspect.getmro(cls) ]
        return cls.merge_dicts(class_lookups)

    def get_lookup(self, lookup_name):
        from django.db.models.lookups import Lookup
        found = self._get_lookup(lookup_name)
        if found is None and hasattr(self, b'output_field'):
            return self.output_field.get_lookup(lookup_name)
        else:
            if found is not None and not issubclass(found, Lookup):
                return
            return found

    def get_transform(self, lookup_name):
        from django.db.models.lookups import Transform
        found = self._get_lookup(lookup_name)
        if found is None and hasattr(self, b'output_field'):
            return self.output_field.get_transform(lookup_name)
        else:
            if found is not None and not issubclass(found, Transform):
                return
            return found

    @staticmethod
    def merge_dicts(dicts):
        """
        Merge dicts in reverse to preference the order of the original list. e.g.,
        merge_dicts([a, b]) will preference the keys in 'a' over those in 'b'.
        """
        merged = {}
        for d in reversed(dicts):
            merged.update(d)

        return merged

    @classmethod
    def _clear_cached_lookups(cls):
        for subclass in subclasses(cls):
            subclass.get_lookups.cache_clear()

    @classmethod
    def register_lookup(cls, lookup, lookup_name=None):
        if lookup_name is None:
            lookup_name = lookup.lookup_name
        if b'class_lookups' not in cls.__dict__:
            cls.class_lookups = {}
        cls.class_lookups[lookup_name] = lookup
        cls._clear_cached_lookups()
        return lookup

    @classmethod
    def _unregister_lookup(cls, lookup, lookup_name=None):
        """
        Remove given lookup from cls lookups. For use in tests only as it's
        not thread-safe.
        """
        if lookup_name is None:
            lookup_name = lookup.lookup_name
        del cls.class_lookups[lookup_name]
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
    if not field.remote_field:
        return False
    if field.remote_field.parent_link and not reverse:
        return False
    if restricted:
        if reverse and field.related_query_name() not in requested:
            return False
        if not reverse and field.name not in requested:
            return False
    if not restricted and field.null:
        return False
    if load_fields:
        if field.attname not in load_fields:
            if restricted and field.name in requested:
                raise InvalidQuery(b'Field %s.%s cannot be both deferred and traversed using select_related at the same time.' % (
                 field.model._meta.object_name, field.name))
    return True


def refs_expression(lookup_parts, annotations):
    """
    A helper method to check if the lookup_parts contains references
    to the given annotations set. Because the LOOKUP_SEP is contained in the
    default annotation names we must check each prefix of the lookup_parts
    for a match.
    """
    for n in range(len(lookup_parts) + 1):
        level_n_lookup = LOOKUP_SEP.join(lookup_parts[0:n])
        if level_n_lookup in annotations and annotations[level_n_lookup]:
            return (annotations[level_n_lookup], lookup_parts[n:])

    return (
     False, ())


def check_rel_lookup_compatibility(model, target_opts, field):
    """
    Check that self.model is compatible with target_opts. Compatibility
    is OK if:
      1) model and opts match (where proxy inheritance is removed)
      2) model is parent of opts' model or the other way around
    """

    def check(opts):
        return model._meta.concrete_model == opts.concrete_model or opts.concrete_model in model._meta.get_parent_list() or model in opts.get_parent_list()

    return check(target_opts) or getattr(field, b'primary_key', False) and check(field.model._meta)
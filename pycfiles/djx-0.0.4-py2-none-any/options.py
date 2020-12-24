# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/db/models/options.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import copy, warnings
from bisect import bisect
from collections import OrderedDict, defaultdict
from itertools import chain
from django.apps import apps
from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from django.db import connections
from django.db.models import Manager
from django.db.models.fields import AutoField
from django.db.models.fields.proxy import OrderWrt
from django.db.models.query_utils import PathInfo
from django.utils import six
from django.utils.datastructures import ImmutableList, OrderedSet
from django.utils.deprecation import RemovedInDjango20Warning, RemovedInDjango21Warning, warn_about_renamed_method
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.text import camel_case_to_spaces, format_lazy
from django.utils.translation import override
NOT_PROVIDED = object()
PROXY_PARENTS = object()
EMPTY_RELATION_TREE = tuple()
IMMUTABLE_WARNING = b"The return type of '%s' should never be mutated. If you want to manipulate this list for your own use, make a copy first."
DEFAULT_NAMES = ('verbose_name', 'verbose_name_plural', 'db_table', 'ordering', 'unique_together',
                 'permissions', 'get_latest_by', 'order_with_respect_to', 'app_label',
                 'db_tablespace', 'abstract', 'managed', 'proxy', 'swappable', 'auto_created',
                 'index_together', 'apps', 'default_permissions', 'select_on_save',
                 'default_related_name', 'required_db_features', 'required_db_vendor',
                 'base_manager_name', 'default_manager_name', 'manager_inheritance_from_future',
                 'indexes')

def normalize_together(option_together):
    """
    option_together can be either a tuple of tuples, or a single
    tuple of two strings. Normalize it to a tuple of tuples, so that
    calling code can uniformly expect that.
    """
    try:
        if not option_together:
            return ()
        else:
            if not isinstance(option_together, (tuple, list)):
                raise TypeError
            first_element = next(iter(option_together))
            if not isinstance(first_element, (tuple, list)):
                option_together = (
                 option_together,)
            return tuple(tuple(ot) for ot in option_together)

    except TypeError:
        return option_together


def make_immutable_fields_list(name, data):
    return ImmutableList(data, warning=IMMUTABLE_WARNING % name)


@python_2_unicode_compatible
class Options(object):
    FORWARD_PROPERTIES = {
     b'fields', b'many_to_many', b'concrete_fields', b'local_concrete_fields',
     b'_forward_fields_map', b'managers', b'managers_map', b'base_manager',
     b'default_manager'}
    REVERSE_PROPERTIES = {
     b'related_objects', b'fields_map', b'_relation_tree'}
    default_apps = apps

    def __init__(self, meta, app_label=None):
        self._get_fields_cache = {}
        self.local_fields = []
        self.local_many_to_many = []
        self.private_fields = []
        self.manager_inheritance_from_future = False
        self.local_managers = []
        self.base_manager_name = None
        self.default_manager_name = None
        self.model_name = None
        self.verbose_name = None
        self.verbose_name_plural = None
        self.db_table = b''
        self.ordering = []
        self._ordering_clash = False
        self.indexes = []
        self.unique_together = []
        self.index_together = []
        self.select_on_save = False
        self.default_permissions = ('add', 'change', 'delete')
        self.permissions = []
        self.object_name = None
        self.app_label = app_label
        self.get_latest_by = None
        self.order_with_respect_to = None
        self.db_tablespace = settings.DEFAULT_TABLESPACE
        self.required_db_features = []
        self.required_db_vendor = None
        self.meta = meta
        self.pk = None
        self.auto_field = None
        self.abstract = False
        self.managed = True
        self.proxy = False
        self.proxy_for_model = None
        self.concrete_model = None
        self.swappable = None
        self.parents = OrderedDict()
        self.auto_created = False
        self.related_fkey_lookups = []
        self.apps = self.default_apps
        self.default_related_name = None
        return

    @property
    def label(self):
        return b'%s.%s' % (self.app_label, self.object_name)

    @property
    def label_lower(self):
        return b'%s.%s' % (self.app_label, self.model_name)

    @property
    def app_config(self):
        return self.apps.app_configs.get(self.app_label)

    @property
    def installed(self):
        return self.app_config is not None

    def contribute_to_class(self, cls, name):
        from django.db import connection
        from django.db.backends.utils import truncate_name
        cls._meta = self
        self.model = cls
        self.object_name = cls.__name__
        self.model_name = self.object_name.lower()
        self.verbose_name = camel_case_to_spaces(self.object_name)
        self.original_attrs = {}
        if self.meta:
            meta_attrs = self.meta.__dict__.copy()
            for name in self.meta.__dict__:
                if name.startswith(b'_'):
                    del meta_attrs[name]

            for attr_name in DEFAULT_NAMES:
                if attr_name in meta_attrs:
                    setattr(self, attr_name, meta_attrs.pop(attr_name))
                    self.original_attrs[attr_name] = getattr(self, attr_name)
                elif hasattr(self.meta, attr_name):
                    setattr(self, attr_name, getattr(self.meta, attr_name))
                    self.original_attrs[attr_name] = getattr(self, attr_name)

            self.unique_together = normalize_together(self.unique_together)
            self.index_together = normalize_together(self.index_together)
            if self.verbose_name_plural is None:
                self.verbose_name_plural = format_lazy(b'{}s', self.verbose_name)
            self._ordering_clash = bool(self.ordering and self.order_with_respect_to)
            if meta_attrs != {}:
                raise TypeError(b"'class Meta' got invalid attribute(s): %s" % (b',').join(meta_attrs.keys()))
        else:
            self.verbose_name_plural = format_lazy(b'{}s', self.verbose_name)
        del self.meta
        if not self.db_table:
            self.db_table = b'%s_%s' % (self.app_label, self.model_name)
            self.db_table = truncate_name(self.db_table, connection.ops.max_name_length())
        return

    def _prepare(self, model):
        if self.order_with_respect_to:
            query = self.order_with_respect_to
            try:
                self.order_with_respect_to = next(f for f in self._get_fields(reverse=False) if f.name == query or f.attname == query)
            except StopIteration:
                raise FieldDoesNotExist(b"%s has no field named '%s'" % (self.object_name, query))

            self.ordering = ('_order', )
            if not any(isinstance(field, OrderWrt) for field in model._meta.local_fields):
                model.add_to_class(b'_order', OrderWrt())
        else:
            self.order_with_respect_to = None
        if self.pk is None:
            if self.parents:
                field = next(six.itervalues(self.parents))
                already_created = [ fld for fld in self.local_fields if fld.name == field.name ]
                if already_created:
                    field = already_created[0]
                field.primary_key = True
                self.setup_pk(field)
                if not field.remote_field.parent_link:
                    warnings.warn(b'Add parent_link=True to %s as an implicit link is deprecated.' % field, RemovedInDjango20Warning)
            else:
                auto = AutoField(verbose_name=b'ID', primary_key=True, auto_created=True)
                model.add_to_class(b'id', auto)
        return

    def add_manager(self, manager):
        self.local_managers.append(manager)
        self._expire_cache()

    def add_field(self, field, private=False, virtual=NOT_PROVIDED):
        if virtual is not NOT_PROVIDED:
            warnings.warn(b'The `virtual` argument of Options.add_field() has been renamed to `private`.', RemovedInDjango20Warning, stacklevel=2)
            private = virtual
        if private:
            self.private_fields.append(field)
        elif field.is_relation and field.many_to_many:
            self.local_many_to_many.insert(bisect(self.local_many_to_many, field), field)
        else:
            self.local_fields.insert(bisect(self.local_fields, field), field)
            self.setup_pk(field)
        if field.is_relation and hasattr(field.remote_field, b'model') and field.remote_field.model:
            try:
                field.remote_field.model._meta._expire_cache(forward=False)
            except AttributeError:
                pass

            self._expire_cache()
        else:
            self._expire_cache(reverse=False)

    def setup_pk(self, field):
        if not self.pk and field.primary_key:
            self.pk = field
            field.serialize = False

    def setup_proxy(self, target):
        """
        Does the internal setup so that the current model is a proxy for
        "target".
        """
        self.pk = target._meta.pk
        self.proxy_for_model = target
        self.db_table = target._meta.db_table

    def __repr__(self):
        return b'<Options for %s>' % self.object_name

    def __str__(self):
        return b'%s.%s' % (self.app_label, self.model_name)

    def can_migrate(self, connection):
        """
        Return True if the model can/should be migrated on the `connection`.
        `connection` can be either a real connection or a connection alias.
        """
        if self.proxy or self.swapped or not self.managed:
            return False
        if isinstance(connection, six.string_types):
            connection = connections[connection]
        if self.required_db_vendor:
            return self.required_db_vendor == connection.vendor
        if self.required_db_features:
            return all(getattr(connection.features, feat, False) for feat in self.required_db_features)
        return True

    @property
    def verbose_name_raw(self):
        """
        There are a few places where the untranslated verbose name is needed
        (so that we get the same value regardless of currently active
        locale).
        """
        with override(None):
            return force_text(self.verbose_name)
        return

    @property
    def swapped(self):
        """
        Has this model been swapped out for another? If so, return the model
        name of the replacement; otherwise, return None.

        For historical reasons, model name lookups using get_model() are
        case insensitive, so we make sure we are case insensitive here.
        """
        if self.swappable:
            swapped_for = getattr(settings, self.swappable, None)
            if swapped_for:
                try:
                    swapped_label, swapped_object = swapped_for.split(b'.')
                except ValueError:
                    return swapped_for

                if b'%s.%s' % (swapped_label, swapped_object.lower()) != self.label_lower:
                    return swapped_for
        return

    @cached_property
    def managers(self):
        managers = []
        seen_managers = set()
        bases = (b for b in self.model.mro() if hasattr(b, b'_meta'))
        for depth, base in enumerate(bases):
            for manager in base._meta.local_managers:
                if manager.name in seen_managers:
                    continue
                manager = copy.copy(manager)
                manager.model = self.model
                seen_managers.add(manager.name)
                managers.append((depth, manager.creation_counter, manager))
                manager._originating_model = base

        return make_immutable_fields_list(b'managers', (m[2] for m in sorted(managers)))

    @cached_property
    def managers_map(self):
        return {manager.name:manager for manager in self.managers}

    @cached_property
    def base_manager(self):
        base_manager_name = self.base_manager_name
        if not base_manager_name:
            for parent in self.model.mro()[1:]:
                if hasattr(parent, b'_meta'):
                    if parent._base_manager.name != b'_base_manager':
                        base_manager_name = parent._base_manager.name
                    break

        if base_manager_name:
            try:
                return self.managers_map[base_manager_name]
            except KeyError:
                raise ValueError(b'%s has no manager named %r' % (
                 self.object_name,
                 base_manager_name))

        for i, base_manager_class in enumerate(self.default_manager.__class__.mro()):
            if getattr(base_manager_class, b'use_for_related_fields', False):
                if not getattr(base_manager_class, b'silence_use_for_related_fields_deprecation', False):
                    warnings.warn((b"use_for_related_fields is deprecated, instead set Meta.base_manager_name on '{}'.").format(self.model._meta.label), RemovedInDjango20Warning, 2)
                if i == 0:
                    manager = self.default_manager
                else:
                    manager = base_manager_class()
                    manager.name = b'_base_manager'
                    manager.model = self.model
                return manager

        manager = Manager()
        manager.name = b'_base_manager'
        manager.model = self.model
        manager.auto_created = True
        return manager

    @cached_property
    def default_manager(self):
        default_manager_name = self.default_manager_name
        if not default_manager_name and not self.local_managers:
            for parent in self.model.mro()[1:]:
                if hasattr(parent, b'_meta'):
                    default_manager_name = parent._meta.default_manager_name
                    break

        if default_manager_name:
            try:
                return self.managers_map[default_manager_name]
            except KeyError:
                raise ValueError(b'%s has no manager named %r' % (
                 self.object_name,
                 default_manager_name))

        if self.managers:
            return self.managers[0]

    @cached_property
    def fields(self):
        """
        Returns a list of all forward fields on the model and its parents,
        excluding ManyToManyFields.

        Private API intended only to be used by Django itself; get_fields()
        combined with filtering of field properties is the public API for
        obtaining this field list.
        """

        def is_not_an_m2m_field(f):
            return not (f.is_relation and f.many_to_many)

        def is_not_a_generic_relation(f):
            return not (f.is_relation and f.one_to_many)

        def is_not_a_generic_foreign_key(f):
            return not (f.is_relation and f.many_to_one and not (hasattr(f.remote_field, b'model') and f.remote_field.model))

        return make_immutable_fields_list(b'fields', (f for f in self._get_fields(reverse=False) if is_not_an_m2m_field(f) and is_not_a_generic_relation(f) and is_not_a_generic_foreign_key(f)))

    @cached_property
    def concrete_fields(self):
        """
        Returns a list of all concrete fields on the model and its parents.

        Private API intended only to be used by Django itself; get_fields()
        combined with filtering of field properties is the public API for
        obtaining this field list.
        """
        return make_immutable_fields_list(b'concrete_fields', (f for f in self.fields if f.concrete))

    @property
    @warn_about_renamed_method(b'Options', b'virtual_fields', b'private_fields', RemovedInDjango20Warning)
    def virtual_fields(self):
        return self.private_fields

    @cached_property
    def local_concrete_fields(self):
        """
        Returns a list of all concrete fields on the model.

        Private API intended only to be used by Django itself; get_fields()
        combined with filtering of field properties is the public API for
        obtaining this field list.
        """
        return make_immutable_fields_list(b'local_concrete_fields', (f for f in self.local_fields if f.concrete))

    @cached_property
    def many_to_many(self):
        """
        Returns a list of all many to many fields on the model and its parents.

        Private API intended only to be used by Django itself; get_fields()
        combined with filtering of field properties is the public API for
        obtaining this list.
        """
        return make_immutable_fields_list(b'many_to_many', (f for f in self._get_fields(reverse=False) if f.is_relation and f.many_to_many))

    @cached_property
    def related_objects(self):
        """
        Returns all related objects pointing to the current model. The related
        objects can come from a one-to-one, one-to-many, or many-to-many field
        relation type.

        Private API intended only to be used by Django itself; get_fields()
        combined with filtering of field properties is the public API for
        obtaining this field list.
        """
        all_related_fields = self._get_fields(forward=False, reverse=True, include_hidden=True)
        return make_immutable_fields_list(b'related_objects', (obj for obj in all_related_fields if not obj.hidden or obj.field.many_to_many))

    @cached_property
    def _forward_fields_map(self):
        res = {}
        fields = self._get_fields(reverse=False)
        for field in fields:
            res[field.name] = field
            try:
                res[field.attname] = field
            except AttributeError:
                pass

        return res

    @cached_property
    def fields_map(self):
        res = {}
        fields = self._get_fields(forward=False, include_hidden=True)
        for field in fields:
            res[field.name] = field
            try:
                res[field.attname] = field
            except AttributeError:
                pass

        return res

    def get_field(self, field_name):
        """
        Return a field instance given the name of a forward or reverse field.
        """
        try:
            return self._forward_fields_map[field_name]
        except KeyError:
            if not self.apps.models_ready:
                raise FieldDoesNotExist(b"%s has no field named '%s'. The app cache isn't ready yet, so if this is an auto-created related field, it won't be available yet." % (
                 self.object_name, field_name))

        try:
            return self.fields_map[field_name]
        except KeyError:
            raise FieldDoesNotExist(b"%s has no field named '%s'" % (self.object_name, field_name))

    def get_base_chain(self, model):
        """
        Return a list of parent classes leading to `model` (ordered from
        closest to most distant ancestor). This has to handle the case where
        `model` is a grandparent or even more distant relation.
        """
        if not self.parents:
            return []
        if model in self.parents:
            return [model]
        for parent in self.parents:
            res = parent._meta.get_base_chain(model)
            if res:
                res.insert(0, parent)
                return res

        return []

    def get_parent_list(self):
        """
        Returns all the ancestors of this model as a list ordered by MRO.
        Useful for determining if something is an ancestor, regardless of lineage.
        """
        result = OrderedSet(self.parents)
        for parent in self.parents:
            for ancestor in parent._meta.get_parent_list():
                result.add(ancestor)

        return list(result)

    def get_ancestor_link(self, ancestor):
        """
        Returns the field on the current model which points to the given
        "ancestor". This is possible an indirect link (a pointer to a parent
        model, which points, eventually, to the ancestor). Used when
        constructing table joins for model inheritance.

        Returns None if the model isn't an ancestor of this one.
        """
        if ancestor in self.parents:
            return self.parents[ancestor]
        for parent in self.parents:
            parent_link = parent._meta.get_ancestor_link(ancestor)
            if parent_link:
                return self.parents[parent] or parent_link

    def get_path_to_parent(self, parent):
        """
        Return a list of PathInfos containing the path from the current
        model to the parent model, or an empty list if parent is not a
        parent of the current model.
        """
        if self.model is parent:
            return []
        proxied_model = self.concrete_model
        path = []
        opts = self
        for int_model in self.get_base_chain(parent):
            if int_model is proxied_model:
                opts = int_model._meta
            else:
                final_field = opts.parents[int_model]
                targets = (final_field.remote_field.get_related_field(),)
                opts = int_model._meta
                path.append(PathInfo(final_field.model._meta, opts, targets, final_field, False, True))

        return path

    def get_path_from_parent(self, parent):
        """
        Return a list of PathInfos containing the path from the parent
        model to the current model, or an empty list if parent is not a
        parent of the current model.
        """
        if self.model is parent:
            return []
        model = self.concrete_model
        chain = model._meta.get_base_chain(parent)
        chain.reverse()
        chain.append(model)
        path = []
        for i, ancestor in enumerate(chain[:-1]):
            child = chain[(i + 1)]
            link = child._meta.get_ancestor_link(ancestor)
            path.extend(link.get_reverse_path_info())

        return path

    def _populate_directed_relation_graph(self):
        """
        This method is used by each model to find its reverse objects. As this
        method is very expensive and is accessed frequently (it looks up every
        field in a model, in every app), it is computed on first access and then
        is set as a property on every model.
        """
        related_objects_graph = defaultdict(list)
        all_models = self.apps.get_models(include_auto_created=True)
        for model in all_models:
            opts = model._meta
            if opts.abstract:
                continue
            fields_with_relations = (f for f in opts._get_fields(reverse=False, include_parents=False) if f.is_relation and f.related_model is not None)
            for f in fields_with_relations:
                if not isinstance(f.remote_field.model, six.string_types):
                    related_objects_graph[f.remote_field.model._meta.concrete_model._meta].append(f)

        for model in all_models:
            related_objects = related_objects_graph[model._meta.concrete_model._meta]
            model._meta.__dict__[b'_relation_tree'] = related_objects

        return self.__dict__.get(b'_relation_tree', EMPTY_RELATION_TREE)

    @cached_property
    def _relation_tree(self):
        return self._populate_directed_relation_graph()

    def _expire_cache(self, forward=True, reverse=True):
        if forward:
            for cache_key in self.FORWARD_PROPERTIES:
                if cache_key in self.__dict__:
                    delattr(self, cache_key)

        if reverse and not self.abstract:
            for cache_key in self.REVERSE_PROPERTIES:
                if cache_key in self.__dict__:
                    delattr(self, cache_key)

        self._get_fields_cache = {}

    def get_fields(self, include_parents=True, include_hidden=False):
        """
        Returns a list of fields associated to the model. By default, includes
        forward and reverse fields, fields derived from inheritance, but not
        hidden fields. The returned fields can be changed using the parameters:

        - include_parents: include fields derived from inheritance
        - include_hidden:  include fields that have a related_name that
                           starts with a "+"
        """
        if include_parents is False:
            include_parents = PROXY_PARENTS
        return self._get_fields(include_parents=include_parents, include_hidden=include_hidden)

    def _get_fields(self, forward=True, reverse=True, include_parents=True, include_hidden=False, seen_models=None):
        """
        Internal helper function to return fields of the model.
        * If forward=True, then fields defined on this model are returned.
        * If reverse=True, then relations pointing to this model are returned.
        * If include_hidden=True, then fields with is_hidden=True are returned.
        * The include_parents argument toggles if fields from parent models
          should be included. It has three values: True, False, and
          PROXY_PARENTS. When set to PROXY_PARENTS, the call will return all
          fields defined for the current model or any of its parents in the
          parent chain to the model's concrete model.
        """
        if include_parents not in (True, False, PROXY_PARENTS):
            raise TypeError(b'Invalid argument for include_parents: %s' % (include_parents,))
        topmost_call = False
        if seen_models is None:
            seen_models = set()
            topmost_call = True
        seen_models.add(self.model)
        cache_key = (
         forward, reverse, include_parents, include_hidden, topmost_call)
        try:
            return self._get_fields_cache[cache_key]
        except KeyError:
            pass

        fields = []
        if include_parents is not False:
            for parent in self.parents:
                if parent in seen_models:
                    continue
                if parent._meta.concrete_model != self.concrete_model and include_parents == PROXY_PARENTS:
                    continue
                for obj in parent._meta._get_fields(forward=forward, reverse=reverse, include_parents=include_parents, include_hidden=include_hidden, seen_models=seen_models):
                    if getattr(obj, b'parent_link', False) and obj.model != self.concrete_model:
                        continue
                    fields.append(obj)

        if reverse and not self.proxy:
            all_fields = self._relation_tree
            for field in all_fields:
                if include_hidden or not field.remote_field.hidden:
                    fields.append(field.remote_field)

        if forward:
            fields.extend(field for field in chain(self.local_fields, self.local_many_to_many))
            if topmost_call:
                fields.extend(f for f in self.private_fields)
        fields = make_immutable_fields_list(b'get_fields()', fields)
        self._get_fields_cache[cache_key] = fields
        return fields

    @property
    def has_auto_field(self):
        warnings.warn(b'Model._meta.has_auto_field is deprecated in favor of checking if Model._meta.auto_field is not None.', RemovedInDjango21Warning, stacklevel=2)
        return self.auto_field is not None

    @has_auto_field.setter
    def has_auto_field(self, value):
        pass

    @cached_property
    def _property_names(self):
        """Return a set of the names of the properties defined on the model."""
        names = []
        for name in dir(self.model):
            try:
                attr = getattr(self.model, name)
            except AttributeError:
                pass
            else:
                if isinstance(attr, property):
                    names.append(name)

        return frozenset(names)
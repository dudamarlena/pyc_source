# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/db/models/fields/related_descriptors.py
# Compiled at: 2019-02-14 00:35:17
"""
Accessors for related objects.

When a field defines a relation between two models, each model class provides
an attribute to access related instances of the other model class (unless the
reverse accessor has been disabled with related_name='+').

Accessors are implemented as descriptors in order to customize access and
assignment. This module defines the descriptor classes.

Forward accessors follow foreign keys. Reverse accessors trace them back. For
example, with the following models::

    class Parent(Model):
        pass

    class Child(Model):
        parent = ForeignKey(Parent, related_name='children')

 ``child.parent`` is a forward many-to-one relation. ``parent.children`` is a
reverse many-to-one relation.

There are three types of relations (many-to-one, one-to-one, and many-to-many)
and two directions (forward and reverse) for a total of six combinations.

1. Related instance on the forward side of a many-to-one relation:
   ``ForwardManyToOneDescriptor``.

   Uniqueness of foreign key values is irrelevant to accessing the related
   instance, making the many-to-one and one-to-one cases identical as far as
   the descriptor is concerned. The constraint is checked upstream (unicity
   validation in forms) or downstream (unique indexes in the database).

2. Related instance on the forward side of a one-to-one
   relation: ``ForwardOneToOneDescriptor``.

   It avoids querying the database when accessing the parent link field in
   a multi-table inheritance scenario.

3. Related instance on the reverse side of a one-to-one relation:
   ``ReverseOneToOneDescriptor``.

   One-to-one relations are asymmetrical, despite the apparent symmetry of the
   name, because they're implemented in the database with a foreign key from
   one table to another. As a consequence ``ReverseOneToOneDescriptor`` is
   slightly different from ``ForwardManyToOneDescriptor``.

4. Related objects manager for related instances on the reverse side of a
   many-to-one relation: ``ReverseManyToOneDescriptor``.

   Unlike the previous two classes, this one provides access to a collection
   of objects. It returns a manager rather than an instance.

5. Related objects manager for related instances on the forward or reverse
   sides of a many-to-many relation: ``ManyToManyDescriptor``.

   Many-to-many relations are symmetrical. The syntax of Django models
   requires declaring them on one side but that's an implementation detail.
   They could be declared on the other side without any change in behavior.
   Therefore the forward and reverse descriptors can be the same.

   If you're looking for ``ForwardManyToManyDescriptor`` or
   ``ReverseManyToManyDescriptor``, use ``ManyToManyDescriptor`` instead.
"""
from __future__ import unicode_literals
import warnings
from operator import attrgetter
from django.db import connections, router, transaction
from django.db.models import Q, signals
from django.db.models.query import QuerySet
from django.utils.deprecation import RemovedInDjango20Warning
from django.utils.functional import cached_property

class ForwardManyToOneDescriptor(object):
    """
    Accessor to the related object on the forward side of a many-to-one or
    one-to-one (via ForwardOneToOneDescriptor subclass) relation.

    In the example::

        class Child(Model):
            parent = ForeignKey(Parent, related_name='children')

    ``child.parent`` is a ``ForwardManyToOneDescriptor`` instance.
    """

    def __init__(self, field_with_rel):
        self.field = field_with_rel
        self.cache_name = self.field.get_cache_name()

    @cached_property
    def RelatedObjectDoesNotExist(self):
        return type(str(b'RelatedObjectDoesNotExist'), (
         self.field.remote_field.model.DoesNotExist, AttributeError), {})

    def is_cached(self, instance):
        return hasattr(instance, self.cache_name)

    def get_queryset(self, **hints):
        related_model = self.field.remote_field.model
        if getattr(related_model._default_manager, b'use_for_related_fields', False):
            if not getattr(related_model._default_manager, b'silence_use_for_related_fields_deprecation', False):
                warnings.warn((b"use_for_related_fields is deprecated, instead set Meta.base_manager_name on '{}'.").format(related_model._meta.label), RemovedInDjango20Warning, 2)
            manager = related_model._default_manager
        else:
            manager = related_model._base_manager
        return manager.db_manager(hints=hints).all()

    def get_prefetch_queryset(self, instances, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        queryset._add_hints(instance=instances[0])
        rel_obj_attr = self.field.get_foreign_related_value
        instance_attr = self.field.get_local_related_value
        instances_dict = {instance_attr(inst):inst for inst in instances}
        related_field = self.field.foreign_related_fields[0]
        if self.field.remote_field.is_hidden() or len(self.field.foreign_related_fields) == 1:
            query = {b'%s__in' % related_field.name: set(instance_attr(inst)[0] for inst in instances)}
        else:
            query = {b'%s__in' % self.field.related_query_name(): instances}
        queryset = queryset.filter(**query)
        if not self.field.remote_field.multiple:
            rel_obj_cache_name = self.field.remote_field.get_cache_name()
            for rel_obj in queryset:
                instance = instances_dict[rel_obj_attr(rel_obj)]
                setattr(rel_obj, rel_obj_cache_name, instance)

        return (
         queryset, rel_obj_attr, instance_attr, True, self.cache_name)

    def get_object(self, instance):
        qs = self.get_queryset(instance=instance)
        return qs.get(self.field.get_reverse_related_filter(instance))

    def __get__(self, instance, cls=None):
        """
        Get the related instance through the forward relation.

        With the example above, when getting ``child.parent``:

        - ``self`` is the descriptor managing the ``parent`` attribute
        - ``instance`` is the ``child`` instance
        - ``cls`` is the ``Child`` class (we don't need it)
        """
        if instance is None:
            return self
        else:
            try:
                rel_obj = getattr(instance, self.cache_name)
            except AttributeError:
                val = self.field.get_local_related_value(instance)
                if None in val:
                    rel_obj = None
                else:
                    rel_obj = self.get_object(instance)
                    if not self.field.remote_field.multiple:
                        setattr(rel_obj, self.field.remote_field.get_cache_name(), instance)
                setattr(instance, self.cache_name, rel_obj)

            if rel_obj is None and not self.field.null:
                raise self.RelatedObjectDoesNotExist(b'%s has no %s.' % (self.field.model.__name__, self.field.name))
            else:
                return rel_obj
            return

    def __set__(self, instance, value):
        """
        Set the related instance through the forward relation.

        With the example above, when setting ``child.parent = parent``:

        - ``self`` is the descriptor managing the ``parent`` attribute
        - ``instance`` is the ``child`` instance
        - ``value`` is the ``parent`` instance on the right of the equal sign
        """
        if value is not None and not isinstance(value, self.field.remote_field.model._meta.concrete_model):
            raise ValueError(b'Cannot assign "%r": "%s.%s" must be a "%s" instance.' % (
             value,
             instance._meta.object_name,
             self.field.name,
             self.field.remote_field.model._meta.object_name))
        else:
            if value is not None:
                if instance._state.db is None:
                    instance._state.db = router.db_for_write(instance.__class__, instance=value)
                elif value._state.db is None:
                    value._state.db = router.db_for_write(value.__class__, instance=instance)
                elif value._state.db is not None and instance._state.db is not None:
                    if not router.allow_relation(value, instance):
                        raise ValueError(b'Cannot assign "%r": the current database router prevents this relation.' % value)
            if value is None:
                related = getattr(instance, self.cache_name, None)
                if related is not None:
                    setattr(related, self.field.remote_field.get_cache_name(), None)
                for lh_field, rh_field in self.field.related_fields:
                    setattr(instance, lh_field.attname, None)

            else:
                for lh_field, rh_field in self.field.related_fields:
                    setattr(instance, lh_field.attname, getattr(value, rh_field.attname))

        setattr(instance, self.cache_name, value)
        if value is not None and not self.field.remote_field.multiple:
            setattr(value, self.field.remote_field.get_cache_name(), instance)
        return


class ForwardOneToOneDescriptor(ForwardManyToOneDescriptor):
    """
    Accessor to the related object on the forward side of a one-to-one relation.

    In the example::

        class Restaurant(Model):
            place = OneToOneField(Place, related_name='restaurant')

    ``restaurant.place`` is a ``ForwardOneToOneDescriptor`` instance.
    """

    def get_object(self, instance):
        if self.field.remote_field.parent_link:
            deferred = instance.get_deferred_fields()
            rel_model = self.field.remote_field.model
            fields = [ field.attname for field in rel_model._meta.concrete_fields ]
            if not any(field in fields for field in deferred):
                kwargs = {field:getattr(instance, field) for field in fields}
                obj = rel_model(**kwargs)
                obj._state.adding = instance._state.adding
                obj._state.db = instance._state.db
                return obj
        return super(ForwardOneToOneDescriptor, self).get_object(instance)


class ReverseOneToOneDescriptor(object):
    """
    Accessor to the related object on the reverse side of a one-to-one
    relation.

    In the example::

        class Restaurant(Model):
            place = OneToOneField(Place, related_name='restaurant')

    ``place.restaurant`` is a ``ReverseOneToOneDescriptor`` instance.
    """

    def __init__(self, related):
        self.related = related
        self.cache_name = related.get_cache_name()

    @cached_property
    def RelatedObjectDoesNotExist(self):
        return type(str(b'RelatedObjectDoesNotExist'), (
         self.related.related_model.DoesNotExist, AttributeError), {})

    def is_cached(self, instance):
        return hasattr(instance, self.cache_name)

    def get_queryset(self, **hints):
        related_model = self.related.related_model
        if getattr(related_model._default_manager, b'use_for_related_fields', False):
            if not getattr(related_model._default_manager, b'silence_use_for_related_fields_deprecation', False):
                warnings.warn((b"use_for_related_fields is deprecated, instead set Meta.base_manager_name on '{}'.").format(related_model._meta.label), RemovedInDjango20Warning, 2)
            manager = related_model._default_manager
        else:
            manager = related_model._base_manager
        return manager.db_manager(hints=hints).all()

    def get_prefetch_queryset(self, instances, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        queryset._add_hints(instance=instances[0])
        rel_obj_attr = attrgetter(self.related.field.attname)

        def instance_attr(obj):
            return obj._get_pk_val()

        instances_dict = {instance_attr(inst):inst for inst in instances}
        query = {b'%s__in' % self.related.field.name: instances}
        queryset = queryset.filter(**query)
        rel_obj_cache_name = self.related.field.get_cache_name()
        for rel_obj in queryset:
            instance = instances_dict[rel_obj_attr(rel_obj)]
            setattr(rel_obj, rel_obj_cache_name, instance)

        return (
         queryset, rel_obj_attr, instance_attr, True, self.cache_name)

    def __get__(self, instance, cls=None):
        """
        Get the related instance through the reverse relation.

        With the example above, when getting ``place.restaurant``:

        - ``self`` is the descriptor managing the ``restaurant`` attribute
        - ``instance`` is the ``place`` instance
        - ``cls`` is the ``Place`` class (unused)

        Keep in mind that ``Restaurant`` holds the foreign key to ``Place``.
        """
        if instance is None:
            return self
        else:
            try:
                rel_obj = getattr(instance, self.cache_name)
            except AttributeError:
                related_pk = instance._get_pk_val()
                if related_pk is None:
                    rel_obj = None
                else:
                    filter_args = self.related.field.get_forward_related_filter(instance)
                    try:
                        rel_obj = self.get_queryset(instance=instance).get(**filter_args)
                    except self.related.related_model.DoesNotExist:
                        rel_obj = None
                    else:
                        setattr(rel_obj, self.related.field.get_cache_name(), instance)

                setattr(instance, self.cache_name, rel_obj)

            if rel_obj is None:
                raise self.RelatedObjectDoesNotExist(b'%s has no %s.' % (
                 instance.__class__.__name__,
                 self.related.get_accessor_name()))
            else:
                return rel_obj
            return

    def __set__(self, instance, value):
        """
        Set the related instance through the reverse relation.

        With the example above, when setting ``place.restaurant = restaurant``:

        - ``self`` is the descriptor managing the ``restaurant`` attribute
        - ``instance`` is the ``place`` instance
        - ``value`` is the ``restaurant`` instance on the right of the equal sign

        Keep in mind that ``Restaurant`` holds the foreign key to ``Place``.
        """
        if value is None:
            try:
                rel_obj = getattr(instance, self.cache_name)
            except AttributeError:
                pass
            else:
                delattr(instance, self.cache_name)
                setattr(rel_obj, self.related.field.name, None)

        elif not isinstance(value, self.related.related_model):
            raise ValueError(b'Cannot assign "%r": "%s.%s" must be a "%s" instance.' % (
             value,
             instance._meta.object_name,
             self.related.get_accessor_name(),
             self.related.related_model._meta.object_name))
        else:
            if instance._state.db is None:
                instance._state.db = router.db_for_write(instance.__class__, instance=value)
            else:
                if value._state.db is None:
                    value._state.db = router.db_for_write(value.__class__, instance=instance)
                elif value._state.db is not None and instance._state.db is not None:
                    if not router.allow_relation(value, instance):
                        raise ValueError(b'Cannot assign "%r": the current database router prevents this relation.' % value)
                related_pk = tuple(getattr(instance, field.attname) for field in self.related.field.foreign_related_fields)
                for index, field in enumerate(self.related.field.local_related_fields):
                    setattr(value, field.attname, related_pk[index])

            setattr(instance, self.cache_name, value)
            setattr(value, self.related.field.get_cache_name(), instance)
        return


class ReverseManyToOneDescriptor(object):
    """
    Accessor to the related objects manager on the reverse side of a
    many-to-one relation.

    In the example::

        class Child(Model):
            parent = ForeignKey(Parent, related_name='children')

    ``parent.children`` is a ``ReverseManyToOneDescriptor`` instance.

    Most of the implementation is delegated to a dynamically defined manager
    class built by ``create_forward_many_to_many_manager()`` defined below.
    """

    def __init__(self, rel):
        self.rel = rel
        self.field = rel.field

    @cached_property
    def related_manager_cls(self):
        related_model = self.rel.related_model
        return create_reverse_many_to_one_manager(related_model._default_manager.__class__, self.rel)

    def __get__(self, instance, cls=None):
        """
        Get the related objects through the reverse relation.

        With the example above, when getting ``parent.children``:

        - ``self`` is the descriptor managing the ``children`` attribute
        - ``instance`` is the ``parent`` instance
        - ``cls`` is the ``Parent`` class (unused)
        """
        if instance is None:
            return self
        else:
            return self.related_manager_cls(instance)

    def _get_set_deprecation_msg_params(self):
        return (
         b'reverse side of a related set',
         self.rel.get_accessor_name())

    def __set__(self, instance, value):
        """
        Set the related objects through the reverse relation.

        With the example above, when setting ``parent.children = children``:

        - ``self`` is the descriptor managing the ``children`` attribute
        - ``instance`` is the ``parent`` instance
        - ``value`` is the ``children`` sequence on the right of the equal sign
        """
        warnings.warn(b'Direct assignment to the %s is deprecated due to the implicit save() that happens. Use %s.set() instead.' % self._get_set_deprecation_msg_params(), RemovedInDjango20Warning, stacklevel=2)
        manager = self.__get__(instance)
        manager.set(value)


def create_reverse_many_to_one_manager(superclass, rel):
    """
    Create a manager for the reverse side of a many-to-one relation.

    This manager subclasses another manager, generally the default manager of
    the related model, and adds behaviors specific to many-to-one relations.
    """

    class RelatedManager(superclass):

        def __init__(self, instance):
            super(RelatedManager, self).__init__()
            self.instance = instance
            self.model = rel.related_model
            self.field = rel.field
            self.core_filters = {self.field.name: instance}

        def __call__(self, **kwargs):
            manager = getattr(self.model, kwargs.pop(b'manager'))
            manager_class = create_reverse_many_to_one_manager(manager.__class__, rel)
            return manager_class(self.instance)

        do_not_call_in_templates = True

        def _apply_rel_filters(self, queryset):
            """
            Filter the queryset for the instance this manager is bound to.
            """
            db = self._db or router.db_for_read(self.model, instance=self.instance)
            empty_strings_as_null = connections[db].features.interprets_empty_strings_as_nulls
            queryset._add_hints(instance=self.instance)
            if self._db:
                queryset = queryset.using(self._db)
            queryset = queryset.filter(**self.core_filters)
            for field in self.field.foreign_related_fields:
                val = getattr(self.instance, field.attname)
                if val is None or val == b'' and empty_strings_as_null:
                    return queryset.none()

            queryset._known_related_objects = {self.field: {self.instance.pk: self.instance}}
            return queryset

        def _remove_prefetched_objects(self):
            try:
                self.instance._prefetched_objects_cache.pop(self.field.related_query_name())
            except (AttributeError, KeyError):
                pass

        def get_queryset(self):
            try:
                return self.instance._prefetched_objects_cache[self.field.related_query_name()]
            except (AttributeError, KeyError):
                queryset = super(RelatedManager, self).get_queryset()
                return self._apply_rel_filters(queryset)

        def get_prefetch_queryset(self, instances, queryset=None):
            if queryset is None:
                queryset = super(RelatedManager, self).get_queryset()
            queryset._add_hints(instance=instances[0])
            queryset = queryset.using(queryset._db or self._db)
            rel_obj_attr = self.field.get_local_related_value
            instance_attr = self.field.get_foreign_related_value
            instances_dict = {instance_attr(inst):inst for inst in instances}
            query = {b'%s__in' % self.field.name: instances}
            queryset = queryset.filter(**query)
            for rel_obj in queryset:
                instance = instances_dict[rel_obj_attr(rel_obj)]
                setattr(rel_obj, self.field.name, instance)

            cache_name = self.field.related_query_name()
            return (queryset, rel_obj_attr, instance_attr, False, cache_name)

        def add(self, *objs, **kwargs):
            self._remove_prefetched_objects()
            bulk = kwargs.pop(b'bulk', True)
            objs = list(objs)
            db = router.db_for_write(self.model, instance=self.instance)

            def check_and_update_obj(obj):
                if not isinstance(obj, self.model):
                    raise TypeError(b"'%s' instance expected, got %r" % (
                     self.model._meta.object_name, obj))
                setattr(obj, self.field.name, self.instance)

            if bulk:
                pks = []
                for obj in objs:
                    check_and_update_obj(obj)
                    if obj._state.adding or obj._state.db != db:
                        raise ValueError(b"%r instance isn't saved. Use bulk=False or save the object first." % obj)
                    pks.append(obj.pk)

                self.model._base_manager.using(db).filter(pk__in=pks).update(**{self.field.name: self.instance})
            else:
                with transaction.atomic(using=db, savepoint=False):
                    for obj in objs:
                        check_and_update_obj(obj)
                        obj.save()

        add.alters_data = True

        def create(self, **kwargs):
            kwargs[self.field.name] = self.instance
            db = router.db_for_write(self.model, instance=self.instance)
            return super(RelatedManager, self.db_manager(db)).create(**kwargs)

        create.alters_data = True

        def get_or_create(self, **kwargs):
            kwargs[self.field.name] = self.instance
            db = router.db_for_write(self.model, instance=self.instance)
            return super(RelatedManager, self.db_manager(db)).get_or_create(**kwargs)

        get_or_create.alters_data = True

        def update_or_create(self, **kwargs):
            kwargs[self.field.name] = self.instance
            db = router.db_for_write(self.model, instance=self.instance)
            return super(RelatedManager, self.db_manager(db)).update_or_create(**kwargs)

        update_or_create.alters_data = True
        if rel.field.null:

            def remove(self, *objs, **kwargs):
                if not objs:
                    return
                bulk = kwargs.pop(b'bulk', True)
                val = self.field.get_foreign_related_value(self.instance)
                old_ids = set()
                for obj in objs:
                    if self.field.get_local_related_value(obj) == val:
                        old_ids.add(obj.pk)
                    else:
                        raise self.field.remote_field.model.DoesNotExist(b'%r is not related to %r.' % (obj, self.instance))

                self._clear(self.filter(pk__in=old_ids), bulk)

            remove.alters_data = True

            def clear(self, **kwargs):
                bulk = kwargs.pop(b'bulk', True)
                self._clear(self, bulk)

            clear.alters_data = True

            def _clear(self, queryset, bulk):
                self._remove_prefetched_objects()
                db = router.db_for_write(self.model, instance=self.instance)
                queryset = queryset.using(db)
                if bulk:
                    queryset.update(**{self.field.name: None})
                else:
                    with transaction.atomic(using=db, savepoint=False):
                        for obj in queryset:
                            setattr(obj, self.field.name, None)
                            obj.save(update_fields=[self.field.name])

                return

            _clear.alters_data = True

        def set(self, objs, **kwargs):
            objs = tuple(objs)
            bulk = kwargs.pop(b'bulk', True)
            clear = kwargs.pop(b'clear', False)
            if self.field.null:
                db = router.db_for_write(self.model, instance=self.instance)
                with transaction.atomic(using=db, savepoint=False):
                    if clear:
                        self.clear()
                        self.add(bulk=bulk, *objs)
                    else:
                        old_objs = set(self.using(db).all())
                        new_objs = []
                        for obj in objs:
                            if obj in old_objs:
                                old_objs.remove(obj)
                            else:
                                new_objs.append(obj)

                        self.remove(bulk=bulk, *old_objs)
                        self.add(bulk=bulk, *new_objs)
            else:
                self.add(bulk=bulk, *objs)

        set.alters_data = True

    return RelatedManager


class ManyToManyDescriptor(ReverseManyToOneDescriptor):
    """
    Accessor to the related objects manager on the forward and reverse sides of
    a many-to-many relation.

    In the example::

        class Pizza(Model):
            toppings = ManyToManyField(Topping, related_name='pizzas')

    ``pizza.toppings`` and ``topping.pizzas`` are ``ManyToManyDescriptor``
    instances.

    Most of the implementation is delegated to a dynamically defined manager
    class built by ``create_forward_many_to_many_manager()`` defined below.
    """

    def __init__(self, rel, reverse=False):
        super(ManyToManyDescriptor, self).__init__(rel)
        self.reverse = reverse

    @property
    def through(self):
        return self.rel.through

    @cached_property
    def related_manager_cls(self):
        related_model = self.rel.related_model if self.reverse else self.rel.model
        return create_forward_many_to_many_manager(related_model._default_manager.__class__, self.rel, reverse=self.reverse)

    def _get_set_deprecation_msg_params(self):
        return (
         b'%s side of a many-to-many set' % (b'reverse' if self.reverse else b'forward'),
         self.rel.get_accessor_name() if self.reverse else self.field.name)


def create_forward_many_to_many_manager(superclass, rel, reverse):
    """
    Create a manager for the either side of a many-to-many relation.

    This manager subclasses another manager, generally the default manager of
    the related model, and adds behaviors specific to many-to-many relations.
    """

    class ManyRelatedManager(superclass):

        def __init__(self, instance=None):
            super(ManyRelatedManager, self).__init__()
            self.instance = instance
            if not reverse:
                self.model = rel.model
                self.query_field_name = rel.field.related_query_name()
                self.prefetch_cache_name = rel.field.name
                self.source_field_name = rel.field.m2m_field_name()
                self.target_field_name = rel.field.m2m_reverse_field_name()
                self.symmetrical = rel.symmetrical
            else:
                self.model = rel.related_model
                self.query_field_name = rel.field.name
                self.prefetch_cache_name = rel.field.related_query_name()
                self.source_field_name = rel.field.m2m_reverse_field_name()
                self.target_field_name = rel.field.m2m_field_name()
                self.symmetrical = False
            self.through = rel.through
            self.reverse = reverse
            self.source_field = self.through._meta.get_field(self.source_field_name)
            self.target_field = self.through._meta.get_field(self.target_field_name)
            self.core_filters = {}
            self.pk_field_names = {}
            for lh_field, rh_field in self.source_field.related_fields:
                core_filter_key = b'%s__%s' % (self.query_field_name, rh_field.name)
                self.core_filters[core_filter_key] = getattr(instance, rh_field.attname)
                self.pk_field_names[lh_field.name] = rh_field.name

            self.related_val = self.source_field.get_foreign_related_value(instance)
            if None in self.related_val:
                raise ValueError(b'"%r" needs to have a value for field "%s" before this many-to-many relationship can be used.' % (
                 instance, self.pk_field_names[self.source_field_name]))
            if instance.pk is None:
                raise ValueError(b'%r instance needs to have a primary key value before a many-to-many relationship can be used.' % instance.__class__.__name__)
            return

        def __call__(self, **kwargs):
            manager = getattr(self.model, kwargs.pop(b'manager'))
            manager_class = create_forward_many_to_many_manager(manager.__class__, rel, reverse)
            return manager_class(instance=self.instance)

        do_not_call_in_templates = True

        def _build_remove_filters(self, removed_vals):
            filters = Q(**{self.source_field_name: self.related_val})
            removed_vals_filters = not isinstance(removed_vals, QuerySet) or removed_vals._has_filters()
            if removed_vals_filters:
                filters &= Q(**{b'%s__in' % self.target_field_name: removed_vals})
            if self.symmetrical:
                symmetrical_filters = Q(**{self.target_field_name: self.related_val})
                if removed_vals_filters:
                    symmetrical_filters &= Q(**{b'%s__in' % self.source_field_name: removed_vals})
                filters |= symmetrical_filters
            return filters

        def _apply_rel_filters(self, queryset):
            """
            Filter the queryset for the instance this manager is bound to.
            """
            queryset._add_hints(instance=self.instance)
            if self._db:
                queryset = queryset.using(self._db)
            return queryset._next_is_sticky().filter(**self.core_filters)

        def _remove_prefetched_objects(self):
            try:
                self.instance._prefetched_objects_cache.pop(self.prefetch_cache_name)
            except (AttributeError, KeyError):
                pass

        def get_queryset(self):
            try:
                return self.instance._prefetched_objects_cache[self.prefetch_cache_name]
            except (AttributeError, KeyError):
                queryset = super(ManyRelatedManager, self).get_queryset()
                return self._apply_rel_filters(queryset)

        def get_prefetch_queryset(self, instances, queryset=None):
            if queryset is None:
                queryset = super(ManyRelatedManager, self).get_queryset()
            queryset._add_hints(instance=instances[0])
            queryset = queryset.using(queryset._db or self._db)
            query = {b'%s__in' % self.query_field_name: instances}
            queryset = queryset._next_is_sticky().filter(**query)
            fk = self.through._meta.get_field(self.source_field_name)
            join_table = fk.model._meta.db_table
            connection = connections[queryset.db]
            qn = connection.ops.quote_name
            queryset = queryset.extra(select={b'_prefetch_related_val_%s' % f.attname:b'%s.%s' % (qn(join_table), qn(f.column)) for f in fk.local_related_fields})
            return (
             queryset,
             lambda result: tuple(getattr(result, b'_prefetch_related_val_%s' % f.attname) for f in fk.local_related_fields),
             lambda inst: tuple(f.get_db_prep_value(getattr(inst, f.attname), connection) for f in fk.foreign_related_fields),
             False,
             self.prefetch_cache_name)

        def add(self, *objs):
            if not rel.through._meta.auto_created:
                opts = self.through._meta
                raise AttributeError(b"Cannot use add() on a ManyToManyField which specifies an intermediary model. Use %s.%s's Manager instead." % (
                 opts.app_label, opts.object_name))
            self._remove_prefetched_objects()
            db = router.db_for_write(self.through, instance=self.instance)
            with transaction.atomic(using=db, savepoint=False):
                self._add_items(self.source_field_name, self.target_field_name, *objs)
                if self.symmetrical:
                    self._add_items(self.target_field_name, self.source_field_name, *objs)

        add.alters_data = True

        def remove(self, *objs):
            if not rel.through._meta.auto_created:
                opts = self.through._meta
                raise AttributeError(b"Cannot use remove() on a ManyToManyField which specifies an intermediary model. Use %s.%s's Manager instead." % (
                 opts.app_label, opts.object_name))
            self._remove_prefetched_objects()
            self._remove_items(self.source_field_name, self.target_field_name, *objs)

        remove.alters_data = True

        def clear(self):
            db = router.db_for_write(self.through, instance=self.instance)
            with transaction.atomic(using=db, savepoint=False):
                signals.m2m_changed.send(sender=self.through, action=b'pre_clear', instance=self.instance, reverse=self.reverse, model=self.model, pk_set=None, using=db)
                self._remove_prefetched_objects()
                filters = self._build_remove_filters(super(ManyRelatedManager, self).get_queryset().using(db))
                self.through._default_manager.using(db).filter(filters).delete()
                signals.m2m_changed.send(sender=self.through, action=b'post_clear', instance=self.instance, reverse=self.reverse, model=self.model, pk_set=None, using=db)
            return

        clear.alters_data = True

        def set(self, objs, **kwargs):
            if not rel.through._meta.auto_created:
                opts = self.through._meta
                raise AttributeError(b"Cannot set values on a ManyToManyField which specifies an intermediary model. Use %s.%s's Manager instead." % (
                 opts.app_label, opts.object_name))
            objs = tuple(objs)
            clear = kwargs.pop(b'clear', False)
            db = router.db_for_write(self.through, instance=self.instance)
            with transaction.atomic(using=db, savepoint=False):
                if clear:
                    self.clear()
                    self.add(*objs)
                else:
                    old_ids = set(self.using(db).values_list(self.target_field.target_field.attname, flat=True))
                    new_objs = []
                    for obj in objs:
                        fk_val = self.target_field.get_foreign_related_value(obj)[0] if isinstance(obj, self.model) else obj
                        if fk_val in old_ids:
                            old_ids.remove(fk_val)
                        else:
                            new_objs.append(obj)

                    self.remove(*old_ids)
                    self.add(*new_objs)

        set.alters_data = True

        def create(self, **kwargs):
            if not self.through._meta.auto_created:
                opts = self.through._meta
                raise AttributeError(b"Cannot use create() on a ManyToManyField which specifies an intermediary model. Use %s.%s's Manager instead." % (
                 opts.app_label, opts.object_name))
            db = router.db_for_write(self.instance.__class__, instance=self.instance)
            new_obj = super(ManyRelatedManager, self.db_manager(db)).create(**kwargs)
            self.add(new_obj)
            return new_obj

        create.alters_data = True

        def get_or_create(self, **kwargs):
            db = router.db_for_write(self.instance.__class__, instance=self.instance)
            obj, created = super(ManyRelatedManager, self.db_manager(db)).get_or_create(**kwargs)
            if created:
                self.add(obj)
            return (
             obj, created)

        get_or_create.alters_data = True

        def update_or_create(self, **kwargs):
            db = router.db_for_write(self.instance.__class__, instance=self.instance)
            obj, created = super(ManyRelatedManager, self.db_manager(db)).update_or_create(**kwargs)
            if created:
                self.add(obj)
            return (
             obj, created)

        update_or_create.alters_data = True

        def _add_items(self, source_field_name, target_field_name, *objs):
            from django.db.models import Model
            if objs:
                new_ids = set()
                for obj in objs:
                    if isinstance(obj, self.model):
                        if not router.allow_relation(obj, self.instance):
                            raise ValueError(b'Cannot add "%r": instance is on database "%s", value is on database "%s"' % (
                             obj, self.instance._state.db, obj._state.db))
                        fk_val = self.through._meta.get_field(target_field_name).get_foreign_related_value(obj)[0]
                        if fk_val is None:
                            raise ValueError(b'Cannot add "%r": the value for field "%s" is None' % (
                             obj, target_field_name))
                        new_ids.add(fk_val)
                    elif isinstance(obj, Model):
                        raise TypeError(b"'%s' instance expected, got %r" % (
                         self.model._meta.object_name, obj))
                    else:
                        new_ids.add(obj)

                db = router.db_for_write(self.through, instance=self.instance)
                vals = self.through._default_manager.using(db).values_list(target_field_name, flat=True).filter(**{source_field_name: self.related_val[0], 
                   b'%s__in' % target_field_name: new_ids})
                new_ids = new_ids - set(vals)
                with transaction.atomic(using=db, savepoint=False):
                    if self.reverse or source_field_name == self.source_field_name:
                        signals.m2m_changed.send(sender=self.through, action=b'pre_add', instance=self.instance, reverse=self.reverse, model=self.model, pk_set=new_ids, using=db)
                    self.through._default_manager.using(db).bulk_create([ self.through(**{b'%s_id' % source_field_name: self.related_val[0], b'%s_id' % target_field_name: obj_id}) for obj_id in new_ids
                                                                        ])
                    if self.reverse or source_field_name == self.source_field_name:
                        signals.m2m_changed.send(sender=self.through, action=b'post_add', instance=self.instance, reverse=self.reverse, model=self.model, pk_set=new_ids, using=db)
            return

        def _remove_items(self, source_field_name, target_field_name, *objs):
            if not objs:
                return
            old_ids = set()
            for obj in objs:
                if isinstance(obj, self.model):
                    fk_val = self.target_field.get_foreign_related_value(obj)[0]
                    old_ids.add(fk_val)
                else:
                    old_ids.add(obj)

            db = router.db_for_write(self.through, instance=self.instance)
            with transaction.atomic(using=db, savepoint=False):
                signals.m2m_changed.send(sender=self.through, action=b'pre_remove', instance=self.instance, reverse=self.reverse, model=self.model, pk_set=old_ids, using=db)
                target_model_qs = super(ManyRelatedManager, self).get_queryset()
                if target_model_qs._has_filters():
                    old_vals = target_model_qs.using(db).filter(**{b'%s__in' % self.target_field.target_field.attname: old_ids})
                else:
                    old_vals = old_ids
                filters = self._build_remove_filters(old_vals)
                self.through._default_manager.using(db).filter(filters).delete()
                signals.m2m_changed.send(sender=self.through, action=b'post_remove', instance=self.instance, reverse=self.reverse, model=self.model, pk_set=old_ids, using=db)

    return ManyRelatedManager
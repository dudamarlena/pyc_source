# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/db/migrations/state.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import copy, warnings
from collections import OrderedDict
from contextlib import contextmanager
from django.apps import AppConfig
from django.apps.registry import Apps, apps as global_apps
from django.conf import settings
from django.db import models
from django.db.models.fields.proxy import OrderWrt
from django.db.models.fields.related import RECURSIVE_RELATIONSHIP_CONSTANT
from django.db.models.options import DEFAULT_NAMES, normalize_together
from django.db.models.utils import make_model_tuple
from django.utils import six
from django.utils.deprecation import RemovedInDjango20Warning
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from django.utils.module_loading import import_string
from django.utils.version import get_docs_version
from .exceptions import InvalidBasesError

def _get_app_label_and_model_name(model, app_label=b''):
    if isinstance(model, six.string_types):
        split = model.split(b'.', 1)
        if len(split) == 2:
            return tuple(split)
        return (app_label, split[0])
    else:
        return (
         model._meta.app_label, model._meta.model_name)


def _get_related_models(m):
    """
    Return all models that have a direct relationship to the given model.
    """
    related_models = [ subclass for subclass in m.__subclasses__() if issubclass(subclass, models.Model)
                     ]
    related_fields_models = set()
    for f in m._meta.get_fields(include_parents=True, include_hidden=True):
        if f.is_relation and f.related_model is not None and not isinstance(f.related_model, six.string_types):
            related_fields_models.add(f.model)
            related_models.append(f.related_model)

    opts = m._meta
    if opts.proxy and m in related_fields_models:
        related_models.append(opts.concrete_model)
    return related_models


def get_related_models_tuples(model):
    """
    Return a list of typical (app_label, model_name) tuples for all related
    models for the given model.
    """
    return {(rel_mod._meta.app_label, rel_mod._meta.model_name) for rel_mod in _get_related_models(model)}


def get_related_models_recursive(model):
    """
    Return all models that have a direct or indirect relationship
    to the given model.

    Relationships are either defined by explicit relational fields, like
    ForeignKey, ManyToManyField or OneToOneField, or by inheriting from another
    model (a superclass is related to its subclasses, but not vice versa). Note,
    however, that a model inheriting from a concrete model is also related to
    its superclass through the implicit *_ptr OneToOneField on the subclass.
    """
    seen = set()
    queue = _get_related_models(model)
    for rel_mod in queue:
        rel_app_label, rel_model_name = rel_mod._meta.app_label, rel_mod._meta.model_name
        if (rel_app_label, rel_model_name) in seen:
            continue
        seen.add((rel_app_label, rel_model_name))
        queue.extend(_get_related_models(rel_mod))

    return seen - {(model._meta.app_label, model._meta.model_name)}


class ProjectState(object):
    """
    Represents the entire project's overall state.
    This is the item that is passed around - we do it here rather than at the
    app level so that cross-app FKs/etc. resolve properly.
    """

    def __init__(self, models=None, real_apps=None):
        self.models = models or {}
        self.real_apps = real_apps or []
        self.is_delayed = False

    def add_model(self, model_state):
        app_label, model_name = model_state.app_label, model_state.name_lower
        self.models[(app_label, model_name)] = model_state
        if b'apps' in self.__dict__:
            self.reload_model(app_label, model_name)

    def remove_model(self, app_label, model_name):
        del self.models[(app_label, model_name)]
        if b'apps' in self.__dict__:
            self.apps.unregister_model(app_label, model_name)
            self.apps.clear_cache()

    def _find_reload_model(self, app_label, model_name, delay=False):
        if delay:
            self.is_delayed = True
        related_models = set()
        try:
            old_model = self.apps.get_model(app_label, model_name)
        except LookupError:
            pass

        if delay:
            related_models = get_related_models_tuples(old_model)
        else:
            related_models = get_related_models_recursive(old_model)
        model_state = self.models[(app_label, model_name)]
        direct_related_models = set()
        for name, field in model_state.fields:
            if field.is_relation:
                if field.remote_field.model == RECURSIVE_RELATIONSHIP_CONSTANT:
                    continue
                rel_app_label, rel_model_name = _get_app_label_and_model_name(field.related_model, app_label)
                direct_related_models.add((rel_app_label, rel_model_name.lower()))

        related_models.update(direct_related_models)
        for rel_app_label, rel_model_name in direct_related_models:
            try:
                rel_model = self.apps.get_model(rel_app_label, rel_model_name)
            except LookupError:
                pass
            else:
                if delay:
                    related_models.update(get_related_models_tuples(rel_model))
                else:
                    related_models.update(get_related_models_recursive(rel_model))

        related_models.add((app_label, model_name))
        return related_models

    def reload_model(self, app_label, model_name, delay=False):
        if b'apps' in self.__dict__:
            related_models = self._find_reload_model(app_label, model_name, delay)
            self._reload(related_models)

    def reload_models(self, models, delay=True):
        if b'apps' in self.__dict__:
            related_models = set()
            for app_label, model_name in models:
                related_models.update(self._find_reload_model(app_label, model_name, delay))

            self._reload(related_models)

    def _reload(self, related_models):
        with self.apps.bulk_update():
            for rel_app_label, rel_model_name in related_models:
                self.apps.unregister_model(rel_app_label, rel_model_name)

        states_to_be_rendered = []
        for model_state in self.apps.real_models:
            if (
             model_state.app_label, model_state.name_lower) in related_models:
                states_to_be_rendered.append(model_state)

        for rel_app_label, rel_model_name in related_models:
            try:
                model_state = self.models[(rel_app_label, rel_model_name)]
            except KeyError:
                pass
            else:
                states_to_be_rendered.append(model_state)

        self.apps.render_multiple(states_to_be_rendered)

    def clone(self):
        """Returns an exact copy of this ProjectState"""
        new_state = ProjectState(models={k:v.clone() for k, v in self.models.items()}, real_apps=self.real_apps)
        if b'apps' in self.__dict__:
            new_state.apps = self.apps.clone()
        new_state.is_delayed = self.is_delayed
        return new_state

    def clear_delayed_apps_cache(self):
        if self.is_delayed and b'apps' in self.__dict__:
            del self.__dict__[b'apps']

    @cached_property
    def apps(self):
        return StateApps(self.real_apps, self.models)

    @property
    def concrete_apps(self):
        self.apps = StateApps(self.real_apps, self.models, ignore_swappable=True)
        return self.apps

    @classmethod
    def from_apps(cls, apps):
        """Takes in an Apps and returns a ProjectState matching it"""
        app_models = {}
        for model in apps.get_models(include_swapped=True):
            model_state = ModelState.from_model(model)
            app_models[(model_state.app_label, model_state.name_lower)] = model_state

        return cls(app_models)

    def __eq__(self, other):
        if set(self.models.keys()) != set(other.models.keys()):
            return False
        if set(self.real_apps) != set(other.real_apps):
            return False
        return all(model == other.models[key] for key, model in self.models.items())

    def __ne__(self, other):
        return not self == other


class AppConfigStub(AppConfig):
    """
    Stubs a Django AppConfig. Only provides a label, and a dict of models.
    """
    path = b''

    def __init__(self, label):
        self.label = label
        super(AppConfigStub, self).__init__(label, None)
        return

    def import_models(self):
        self.models = self.apps.all_models[self.label]


class StateApps(Apps):
    """
    Subclass of the global Apps registry class to better handle dynamic model
    additions and removals.
    """

    def __init__(self, real_apps, models, ignore_swappable=False):
        self.real_models = []
        for app_label in real_apps:
            app = global_apps.get_app_config(app_label)
            for model in app.get_models():
                self.real_models.append(ModelState.from_model(model, exclude_rels=True))

        app_labels = {model_state.app_label for model_state in models.values()}
        app_configs = [ AppConfigStub(label) for label in sorted(real_apps + list(app_labels)) ]
        super(StateApps, self).__init__(app_configs)
        self._lock = None
        self.render_multiple(list(models.values()) + self.real_models)
        from django.core.checks.model_checks import _check_lazy_references
        ignore = {make_model_tuple(settings.AUTH_USER_MODEL)} if ignore_swappable else set()
        errors = _check_lazy_references(self, ignore=ignore)
        if errors:
            raise ValueError((b'\n').join(error.msg for error in errors))
        return

    @contextmanager
    def bulk_update(self):
        ready = self.ready
        self.ready = False
        try:
            yield
        finally:
            self.ready = ready
            self.clear_cache()

    def render_multiple(self, model_states):
        if not model_states:
            return
        with self.bulk_update():
            unrendered_models = model_states
            while unrendered_models:
                new_unrendered_models = []
                for model in unrendered_models:
                    try:
                        model.render(self)
                    except InvalidBasesError:
                        new_unrendered_models.append(model)

                if len(new_unrendered_models) == len(unrendered_models):
                    raise InvalidBasesError(b'Cannot resolve bases for %r\nThis can happen if you are inheriting models from an app with migrations (e.g. contrib.auth)\n in an app with no migrations; see https://docs.djangoproject.com/en/%s/topics/migrations/#dependencies for more' % (
                     new_unrendered_models, get_docs_version()))
                unrendered_models = new_unrendered_models

    def clone(self):
        """
        Return a clone of this registry, mainly used by the migration framework.
        """
        clone = StateApps([], {})
        clone.all_models = copy.deepcopy(self.all_models)
        clone.app_configs = copy.deepcopy(self.app_configs)
        for app_config in clone.app_configs.values():
            app_config.apps = clone

        clone.real_models = self.real_models
        return clone

    def register_model(self, app_label, model):
        self.all_models[app_label][model._meta.model_name] = model
        if app_label not in self.app_configs:
            self.app_configs[app_label] = AppConfigStub(app_label)
            self.app_configs[app_label].apps = self
            self.app_configs[app_label].models = OrderedDict()
        self.app_configs[app_label].models[model._meta.model_name] = model
        self.do_pending_operations(model)
        self.clear_cache()

    def unregister_model(self, app_label, model_name):
        try:
            del self.all_models[app_label][model_name]
            del self.app_configs[app_label].models[model_name]
        except KeyError:
            pass


class ModelState(object):
    """
    Represents a Django Model. We don't use the actual Model class
    as it's not designed to have its options changed - instead, we
    mutate this one and then render it into a Model as required.

    Note that while you are allowed to mutate .fields, you are not allowed
    to mutate the Field instances inside there themselves - you must instead
    assign new ones, as these are not detached during a clone.
    """

    def __init__(self, app_label, name, fields, options=None, bases=None, managers=None):
        self.app_label = app_label
        self.name = force_text(name)
        self.fields = fields
        self.options = options or {}
        self.options.setdefault(b'indexes', [])
        self.bases = bases or (models.Model,)
        self.managers = managers or []
        if isinstance(self.fields, dict):
            raise ValueError(b'ModelState.fields cannot be a dict - it must be a list of 2-tuples.')
        for name, field in fields:
            if hasattr(field, b'model'):
                raise ValueError(b'ModelState.fields cannot be bound to a model - "%s" is.' % name)
            if field.is_relation and hasattr(field.related_model, b'_meta'):
                raise ValueError(b'ModelState.fields cannot refer to a model class - "%s.to" does. Use a string reference instead.' % name)
            if field.many_to_many and hasattr(field.remote_field.through, b'_meta'):
                raise ValueError(b'ModelState.fields cannot refer to a model class - "%s.through" does. Use a string reference instead.' % name)

        for index in self.options[b'indexes']:
            if not index.name:
                raise ValueError(b"Indexes passed to ModelState require a name attribute. %r doesn't have one." % index)

    @cached_property
    def name_lower(self):
        return self.name.lower()

    @classmethod
    def from_model(cls, model, exclude_rels=False):
        """
        Feed me a model, get a ModelState representing it out.
        """
        fields = []
        for field in model._meta.local_fields:
            if getattr(field, b'remote_field', None) and exclude_rels:
                continue
            if isinstance(field, OrderWrt):
                continue
            name = force_text(field.name, strings_only=True)
            try:
                fields.append((name, field.clone()))
            except TypeError as e:
                raise TypeError(b"Couldn't reconstruct field %s on %s: %s" % (
                 name,
                 model._meta.label,
                 e))

        if not exclude_rels:
            for field in model._meta.local_many_to_many:
                name = force_text(field.name, strings_only=True)
                try:
                    fields.append((name, field.clone()))
                except TypeError as e:
                    raise TypeError(b"Couldn't reconstruct m2m field %s on %s: %s" % (
                     name,
                     model._meta.object_name,
                     e))

        options = {}
        for name in DEFAULT_NAMES:
            if name in ('apps', 'app_label'):
                continue
            elif name in model._meta.original_attrs:
                if name == b'unique_together':
                    ut = model._meta.original_attrs[b'unique_together']
                    options[name] = set(normalize_together(ut))
                elif name == b'index_together':
                    it = model._meta.original_attrs[b'index_together']
                    options[name] = set(normalize_together(it))
                elif name == b'indexes':
                    indexes = [ idx.clone() for idx in model._meta.indexes ]
                    for index in indexes:
                        if not index.name:
                            index.set_name_with_model(model)

                    options[b'indexes'] = indexes
                else:
                    options[name] = model._meta.original_attrs[name]

        options = cls.force_text_recursive(options)
        if exclude_rels:
            for key in [b'unique_together', b'index_together', b'order_with_respect_to']:
                if key in options:
                    del options[key]

        else:
            if options.get(b'order_with_respect_to') in {field.name for field in model._meta.private_fields}:
                del options[b'order_with_respect_to']

            def flatten_bases(model):
                bases = []
                for base in model.__bases__:
                    if hasattr(base, b'_meta') and base._meta.abstract:
                        bases.extend(flatten_bases(base))
                    else:
                        bases.append(base)

                return bases

            flattened_bases = sorted(set(flatten_bases(model)), key=lambda x: model.__mro__.index(x))
            bases = tuple((base._meta.label_lower if hasattr(base, b'_meta') else base) for base in flattened_bases)
            if not any(isinstance(base, six.string_types) or issubclass(base, models.Model) for base in bases):
                bases = (
                 models.Model,)
            managers = []
            manager_names = set()
            default_manager_shim = None
            for manager in model._meta.managers:
                manager_name = force_text(manager.name)
                if manager_name in manager_names:
                    continue
                elif manager.use_in_migrations:
                    new_manager = copy.copy(manager)
                    new_manager._set_creation_counter()
                elif manager is model._base_manager or manager is model._default_manager:
                    new_manager = models.Manager()
                    new_manager.model = manager.model
                    new_manager.name = manager.name
                    if manager is model._default_manager:
                        default_manager_shim = new_manager
                else:
                    continue
                manager_names.add(manager_name)
                managers.append((manager_name, new_manager))

        if managers == [(b'objects', default_manager_shim)]:
            managers = []
        return cls(model._meta.app_label, model._meta.object_name, fields, options, bases, managers)

    @classmethod
    def force_text_recursive(cls, value):
        if isinstance(value, six.string_types):
            return force_text(value)
        if isinstance(value, list):
            return [ cls.force_text_recursive(x) for x in value ]
        if isinstance(value, tuple):
            return tuple(cls.force_text_recursive(x) for x in value)
        if isinstance(value, set):
            return set(cls.force_text_recursive(x) for x in value)
        if isinstance(value, dict):
            return {cls.force_text_recursive(k):cls.force_text_recursive(v) for k, v in value.items()}
        return value

    def construct_managers(self):
        """Deep-clone the managers using deconstruction"""
        sorted_managers = sorted(self.managers, key=lambda v: v[1].creation_counter)
        for mgr_name, manager in sorted_managers:
            mgr_name = force_text(mgr_name)
            as_manager, manager_path, qs_path, args, kwargs = manager.deconstruct()
            if as_manager:
                qs_class = import_string(qs_path)
                yield (mgr_name, qs_class.as_manager())
            else:
                manager_class = import_string(manager_path)
                yield (mgr_name, manager_class(*args, **kwargs))

    def clone(self):
        """Returns an exact copy of this ModelState"""
        return self.__class__(app_label=self.app_label, name=self.name, fields=list(self.fields), options=dict(self.options), bases=self.bases, managers=list(self.managers))

    def render(self, apps):
        """Creates a Model object from our current state into the given apps"""
        meta_contents = {b'app_label': self.app_label, b'apps': apps}
        meta_contents.update(self.options)
        meta = type(str(b'Meta'), tuple(), meta_contents)
        try:
            bases = tuple((apps.get_model(base) if isinstance(base, six.string_types) else base) for base in self.bases)
        except LookupError:
            raise InvalidBasesError(b'Cannot resolve one or more bases from %r' % (self.bases,))

        body = {name:field.clone() for name, field in self.fields}
        body[b'Meta'] = meta
        body[b'__module__'] = b'__fake__'
        body.update(self.construct_managers())
        with warnings.catch_warnings():
            warnings.filterwarnings(b'ignore', b'Managers from concrete parents will soon qualify as default managers', RemovedInDjango20Warning)
            return type(str(self.name), bases, body)

    def get_field_by_name(self, name):
        for fname, field in self.fields:
            if fname == name:
                return field

        raise ValueError(b'No field called %s on model %s' % (name, self.name))

    def get_index_by_name(self, name):
        for index in self.options[b'indexes']:
            if index.name == name:
                return index

        raise ValueError(b'No index named %s on model %s' % (name, self.name))

    def __repr__(self):
        return b"<%s: '%s.%s'>" % (self.__class__.__name__, self.app_label, self.name)

    def __eq__(self, other):
        return self.app_label == other.app_label and self.name == other.name and len(self.fields) == len(other.fields) and all(k1 == k2 and f1.deconstruct()[1:] == f2.deconstruct()[1:] for (k1, f1), (k2, f2) in zip(self.fields, other.fields)) and self.options == other.options and self.bases == other.bases and self.managers == other.managers

    def __ne__(self, other):
        return not self == other
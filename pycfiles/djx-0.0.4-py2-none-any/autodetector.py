# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/db/migrations/autodetector.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import functools, re
from itertools import chain
from django.conf import settings
from django.db import models
from django.db.migrations import operations
from django.db.migrations.migration import Migration
from django.db.migrations.operations.models import AlterModelOptions
from django.db.migrations.optimizer import MigrationOptimizer
from django.db.migrations.questioner import MigrationQuestioner
from django.db.migrations.utils import COMPILED_REGEX_TYPE, RegexObject, get_migration_name_timestamp
from django.utils import six
from .topological_sort import stable_topological_sort

class MigrationAutodetector(object):
    """
    Takes a pair of ProjectStates, and compares them to see what the
    first would need doing to make it match the second (the second
    usually being the project's current state).

    Note that this naturally operates on entire projects at a time,
    as it's likely that changes interact (for example, you can't
    add a ForeignKey without having a migration to add the table it
    depends on first). A user interface may offer single-app usage
    if it wishes, with the caveat that it may not always be possible.
    """

    def __init__(self, from_state, to_state, questioner=None):
        self.from_state = from_state
        self.to_state = to_state
        self.questioner = questioner or MigrationQuestioner()
        self.existing_apps = {app for app, model in from_state.models}

    def changes(self, graph, trim_to_apps=None, convert_apps=None, migration_name=None):
        """
        Main entry point to produce a list of applicable changes.
        Takes a graph to base names on and an optional set of apps
        to try and restrict to (restriction is not guaranteed)
        """
        changes = self._detect_changes(convert_apps, graph)
        changes = self.arrange_for_graph(changes, graph, migration_name)
        if trim_to_apps:
            changes = self._trim_to_apps(changes, trim_to_apps)
        return changes

    def deep_deconstruct(self, obj):
        """
        Recursive deconstruction for a field and its arguments.
        Used for full comparison for rename/alter; sometimes a single-level
        deconstruction will not compare correctly.
        """
        if isinstance(obj, list):
            return [ self.deep_deconstruct(value) for value in obj ]
        else:
            if isinstance(obj, tuple):
                return tuple(self.deep_deconstruct(value) for value in obj)
            if isinstance(obj, dict):
                return {key:self.deep_deconstruct(value) for key, value in obj.items()}
            if isinstance(obj, functools.partial):
                return (obj.func, self.deep_deconstruct(obj.args), self.deep_deconstruct(obj.keywords))
            if isinstance(obj, COMPILED_REGEX_TYPE):
                return RegexObject(obj)
            if isinstance(obj, type):
                return obj
            if hasattr(obj, b'deconstruct'):
                deconstructed = obj.deconstruct()
                if isinstance(obj, models.Field):
                    deconstructed = deconstructed[1:]
                path, args, kwargs = deconstructed
                return (
                 path, [ self.deep_deconstruct(value) for value in args ],
                 {key:self.deep_deconstruct(value) for key, value in kwargs.items()})
            return obj

    def only_relation_agnostic_fields(self, fields):
        """
        Return a definition of the fields that ignores field names and
        what related fields actually relate to.
        Used for detecting renames (as, of course, the related fields
        change during renames)
        """
        fields_def = []
        for name, field in sorted(fields):
            deconstruction = self.deep_deconstruct(field)
            if field.remote_field and field.remote_field.model:
                del deconstruction[2][b'to']
            fields_def.append(deconstruction)

        return fields_def

    def _detect_changes(self, convert_apps=None, graph=None):
        """
        Returns a dict of migration plans which will achieve the
        change from from_state to to_state. The dict has app labels
        as keys and a list of migrations as values.

        The resulting migrations aren't specially named, but the names
        do matter for dependencies inside the set.

        convert_apps is the list of apps to convert to use migrations
        (i.e. to make initial migrations for, in the usual case)

        graph is an optional argument that, if provided, can help improve
        dependency generation and avoid potential circular dependencies.
        """
        self.generated_operations = {}
        self.altered_indexes = {}
        self.old_apps = self.from_state.concrete_apps
        self.new_apps = self.to_state.apps
        self.old_model_keys = []
        self.old_proxy_keys = []
        self.old_unmanaged_keys = []
        self.new_model_keys = []
        self.new_proxy_keys = []
        self.new_unmanaged_keys = []
        for al, mn in sorted(self.from_state.models.keys()):
            model = self.old_apps.get_model(al, mn)
            if not model._meta.managed:
                self.old_unmanaged_keys.append((al, mn))
            elif al not in self.from_state.real_apps:
                if model._meta.proxy:
                    self.old_proxy_keys.append((al, mn))
                else:
                    self.old_model_keys.append((al, mn))

        for al, mn in sorted(self.to_state.models.keys()):
            model = self.new_apps.get_model(al, mn)
            if not model._meta.managed:
                self.new_unmanaged_keys.append((al, mn))
            elif al not in self.from_state.real_apps or convert_apps and al in convert_apps:
                if model._meta.proxy:
                    self.new_proxy_keys.append((al, mn))
                else:
                    self.new_model_keys.append((al, mn))

        self.generate_renamed_models()
        self._prepare_field_lists()
        self._generate_through_model_map()
        self.generate_deleted_models()
        self.generate_created_models()
        self.generate_deleted_proxies()
        self.generate_created_proxies()
        self.generate_altered_options()
        self.generate_altered_managers()
        self.create_altered_indexes()
        self.generate_removed_indexes()
        self.generate_renamed_fields()
        self.generate_removed_fields()
        self.generate_added_fields()
        self.generate_altered_fields()
        self.generate_altered_unique_together()
        self.generate_altered_index_together()
        self.generate_added_indexes()
        self.generate_altered_db_table()
        self.generate_altered_order_with_respect_to()
        self._sort_migrations()
        self._build_migration_list(graph)
        self._optimize_migrations()
        return self.migrations

    def _prepare_field_lists(self):
        """
        Prepare field lists, and prepare a list of the fields that used
        through models in the old state so we can make dependencies
        from the through model deletion to the field that uses it.
        """
        self.kept_model_keys = set(self.old_model_keys).intersection(self.new_model_keys)
        self.kept_proxy_keys = set(self.old_proxy_keys).intersection(self.new_proxy_keys)
        self.kept_unmanaged_keys = set(self.old_unmanaged_keys).intersection(self.new_unmanaged_keys)
        self.through_users = {}
        self.old_field_keys = set()
        self.new_field_keys = set()
        for app_label, model_name in sorted(self.kept_model_keys):
            old_model_name = self.renamed_models.get((app_label, model_name), model_name)
            old_model_state = self.from_state.models[(app_label, old_model_name)]
            new_model_state = self.to_state.models[(app_label, model_name)]
            self.old_field_keys.update((app_label, model_name, x) for x, y in old_model_state.fields)
            self.new_field_keys.update((app_label, model_name, x) for x, y in new_model_state.fields)

    def _generate_through_model_map(self):
        """
        Through model map generation
        """
        for app_label, model_name in sorted(self.old_model_keys):
            old_model_name = self.renamed_models.get((app_label, model_name), model_name)
            old_model_state = self.from_state.models[(app_label, old_model_name)]
            for field_name, field in old_model_state.fields:
                old_field = self.old_apps.get_model(app_label, old_model_name)._meta.get_field(field_name)
                if hasattr(old_field, b'remote_field') and getattr(old_field.remote_field, b'through', None) and not old_field.remote_field.through._meta.auto_created:
                    through_key = (old_field.remote_field.through._meta.app_label,
                     old_field.remote_field.through._meta.model_name)
                    self.through_users[through_key] = (
                     app_label, old_model_name, field_name)

        return

    def _build_migration_list(self, graph=None):
        """
        We need to chop the lists of operations up into migrations with
        dependencies on each other. We do this by stepping up an app's list of
        operations until we find one that has an outgoing dependency that isn't
        in another app's migration yet (hasn't been chopped off its list). We
        then chop off the operations before it into a migration and move onto
        the next app. If we loop back around without doing anything, there's a
        circular dependency (which _should_ be impossible as the operations are
        all split at this point so they can't depend and be depended on).
        """
        self.migrations = {}
        num_ops = sum(len(x) for x in self.generated_operations.values())
        chop_mode = False
        while num_ops:
            for app_label in sorted(self.generated_operations.keys()):
                chopped = []
                dependencies = set()
                for operation in list(self.generated_operations[app_label]):
                    deps_satisfied = True
                    operation_dependencies = set()
                    for dep in operation._auto_deps:
                        is_swappable_dep = False
                        if dep[0] == b'__setting__':
                            resolved_app_label, resolved_object_name = getattr(settings, dep[1]).split(b'.')
                            original_dep = dep
                            dep = (resolved_app_label, resolved_object_name.lower(), dep[2], dep[3])
                            is_swappable_dep = True
                        if dep[0] != app_label and dep[0] != b'__setting__':
                            for other_operation in self.generated_operations.get(dep[0], []):
                                if self.check_dependency(other_operation, dep):
                                    deps_satisfied = False
                                    break

                            if not deps_satisfied:
                                break
                            elif is_swappable_dep:
                                operation_dependencies.add((original_dep[0], original_dep[1]))
                            elif dep[0] in self.migrations:
                                operation_dependencies.add((dep[0], self.migrations[dep[0]][(-1)].name))
                            elif chop_mode:
                                if graph and graph.leaf_nodes(dep[0]):
                                    operation_dependencies.add(graph.leaf_nodes(dep[0])[0])
                                else:
                                    operation_dependencies.add((dep[0], b'__first__'))
                            else:
                                deps_satisfied = False

                    if deps_satisfied:
                        chopped.append(operation)
                        dependencies.update(operation_dependencies)
                        self.generated_operations[app_label] = self.generated_operations[app_label][1:]
                    else:
                        break

                if dependencies or chopped:
                    if not self.generated_operations[app_label] or chop_mode:
                        subclass = type(str(b'Migration'), (Migration,), {b'operations': [], b'dependencies': []})
                        instance = subclass(b'auto_%i' % (len(self.migrations.get(app_label, [])) + 1), app_label)
                        instance.dependencies = list(dependencies)
                        instance.operations = chopped
                        instance.initial = app_label not in self.existing_apps
                        self.migrations.setdefault(app_label, []).append(instance)
                        chop_mode = False
                    else:
                        self.generated_operations[app_label] = chopped + self.generated_operations[app_label]

            new_num_ops = sum(len(x) for x in self.generated_operations.values())
            if new_num_ops == num_ops:
                if not chop_mode:
                    chop_mode = True
                else:
                    raise ValueError(b'Cannot resolve operation dependencies: %r' % self.generated_operations)
            num_ops = new_num_ops

    def _sort_migrations(self):
        """
        Reorder to make things possible. The order we have already isn't bad,
        but we need to pull a few things around so FKs work nicely inside the
        same app
        """
        for app_label, ops in sorted(self.generated_operations.items()):
            dependency_graph = {op:set() for op in ops}
            for op in ops:
                for dep in op._auto_deps:
                    if dep[0] == app_label:
                        for op2 in ops:
                            if self.check_dependency(op2, dep):
                                dependency_graph[op].add(op2)

            self.generated_operations[app_label] = stable_topological_sort(ops, dependency_graph)

    def _optimize_migrations(self):
        for app_label, migrations in self.migrations.items():
            for m1, m2 in zip(migrations, migrations[1:]):
                m2.dependencies.append((app_label, m1.name))

        for app_label, migrations in self.migrations.items():
            for migration in migrations:
                migration.dependencies = list(set(migration.dependencies))

        for app_label, migrations in self.migrations.items():
            for migration in migrations:
                migration.operations = MigrationOptimizer().optimize(migration.operations, app_label=app_label)

    def check_dependency(self, operation, dependency):
        """
        Returns ``True`` if the given operation depends on the given dependency,
        ``False`` otherwise.
        """
        if dependency[2] is None and dependency[3] is True:
            return isinstance(operation, operations.CreateModel) and operation.name_lower == dependency[1].lower()
        else:
            if dependency[2] is not None and dependency[3] is True:
                return isinstance(operation, operations.CreateModel) and operation.name_lower == dependency[1].lower() and any(dependency[2] == x for x, y in operation.fields) or isinstance(operation, operations.AddField) and operation.model_name_lower == dependency[1].lower() and operation.name_lower == dependency[2].lower()
            if dependency[2] is not None and dependency[3] is False:
                return isinstance(operation, operations.RemoveField) and operation.model_name_lower == dependency[1].lower() and operation.name_lower == dependency[2].lower()
            if dependency[2] is None and dependency[3] is False:
                return isinstance(operation, operations.DeleteModel) and operation.name_lower == dependency[1].lower()
            if dependency[2] is not None and dependency[3] == b'alter':
                return isinstance(operation, operations.AlterField) and operation.model_name_lower == dependency[1].lower() and operation.name_lower == dependency[2].lower()
            if dependency[2] is not None and dependency[3] == b'order_wrt_unset':
                return isinstance(operation, operations.AlterOrderWithRespectTo) and operation.name_lower == dependency[1].lower() and (operation.order_with_respect_to or b'').lower() != dependency[2].lower()
            if dependency[2] is not None and dependency[3] == b'foo_together_change':
                return isinstance(operation, (operations.AlterUniqueTogether,
                 operations.AlterIndexTogether)) and operation.name_lower == dependency[1].lower()
            raise ValueError(b"Can't handle dependency %r" % (dependency,))
            return

    def add_operation(self, app_label, operation, dependencies=None, beginning=False):
        operation._auto_deps = dependencies or []
        if beginning:
            self.generated_operations.setdefault(app_label, []).insert(0, operation)
        else:
            self.generated_operations.setdefault(app_label, []).append(operation)

    def swappable_first_key(self, item):
        """
        Sorting key function that places potential swappable models first in
        lists of created models (only real way to solve #22783)
        """
        try:
            model = self.new_apps.get_model(item[0], item[1])
            base_names = [ base.__name__ for base in model.__bases__ ]
            string_version = b'%s.%s' % (item[0], item[1])
            if model._meta.swappable or b'AbstractUser' in base_names or b'AbstractBaseUser' in base_names or settings.AUTH_USER_MODEL.lower() == string_version.lower():
                return (
                 b'___' + item[0], b'___' + item[1])
        except LookupError:
            pass

        return item

    def generate_renamed_models(self):
        """
        Finds any renamed models, and generates the operations for them,
        and removes the old entry from the model lists.
        Must be run before other model-level generation.
        """
        self.renamed_models = {}
        self.renamed_models_rel = {}
        added_models = set(self.new_model_keys) - set(self.old_model_keys)
        for app_label, model_name in sorted(added_models):
            model_state = self.to_state.models[(app_label, model_name)]
            model_fields_def = self.only_relation_agnostic_fields(model_state.fields)
            removed_models = set(self.old_model_keys) - set(self.new_model_keys)
            for rem_app_label, rem_model_name in removed_models:
                if rem_app_label == app_label:
                    rem_model_state = self.from_state.models[(rem_app_label, rem_model_name)]
                    rem_model_fields_def = self.only_relation_agnostic_fields(rem_model_state.fields)
                    if model_fields_def == rem_model_fields_def:
                        if self.questioner.ask_rename_model(rem_model_state, model_state):
                            self.add_operation(app_label, operations.RenameModel(old_name=rem_model_state.name, new_name=model_state.name))
                            self.renamed_models[(app_label, model_name)] = rem_model_name
                            renamed_models_rel_key = b'%s.%s' % (rem_model_state.app_label, rem_model_state.name)
                            self.renamed_models_rel[renamed_models_rel_key] = b'%s.%s' % (
                             model_state.app_label,
                             model_state.name)
                            self.old_model_keys.remove((rem_app_label, rem_model_name))
                            self.old_model_keys.append((app_label, model_name))
                            break

    def generate_created_models(self):
        """
        Find all new models (both managed and unmanaged) and make create
        operations for them as well as separate operations to create any
        foreign key or M2M relationships (we'll optimize these back in later
        if we can).

        We also defer any model options that refer to collections of fields
        that might be deferred (e.g. unique_together, index_together).
        """
        old_keys = set(self.old_model_keys).union(self.old_unmanaged_keys)
        added_models = set(self.new_model_keys) - old_keys
        added_unmanaged_models = set(self.new_unmanaged_keys) - old_keys
        all_added_models = chain(sorted(added_models, key=self.swappable_first_key, reverse=True), sorted(added_unmanaged_models, key=self.swappable_first_key, reverse=True))
        for app_label, model_name in all_added_models:
            model_state = self.to_state.models[(app_label, model_name)]
            model_opts = self.new_apps.get_model(app_label, model_name)._meta
            related_fields = {}
            primary_key_rel = None
            for field in model_opts.local_fields:
                if field.remote_field:
                    if field.remote_field.model:
                        if field.primary_key:
                            primary_key_rel = field.remote_field.model
                        elif not field.remote_field.parent_link:
                            related_fields[field.name] = field
                    if getattr(field.remote_field, b'through', None) and not field.remote_field.through._meta.auto_created:
                        related_fields[field.name] = field

            for field in model_opts.local_many_to_many:
                if field.remote_field.model:
                    related_fields[field.name] = field
                if getattr(field.remote_field, b'through', None) and not field.remote_field.through._meta.auto_created:
                    related_fields[field.name] = field

            indexes = model_state.options.pop(b'indexes')
            unique_together = model_state.options.pop(b'unique_together', None)
            index_together = model_state.options.pop(b'index_together', None)
            order_with_respect_to = model_state.options.pop(b'order_with_respect_to', None)
            dependencies = [
             (
              app_label, model_name, None, False)]
            for base in model_state.bases:
                if isinstance(base, six.string_types) and b'.' in base:
                    base_app_label, base_name = base.split(b'.', 1)
                    dependencies.append((base_app_label, base_name, None, True))

            if primary_key_rel:
                dependencies.append((
                 primary_key_rel._meta.app_label,
                 primary_key_rel._meta.object_name,
                 None,
                 True))
            self.add_operation(app_label, operations.CreateModel(name=model_state.name, fields=[ d for d in model_state.fields if d[0] not in related_fields ], options=model_state.options, bases=model_state.bases, managers=model_state.managers), dependencies=dependencies, beginning=True)
            if not model_opts.managed:
                continue
            for name, field in sorted(related_fields.items()):
                dependencies = self._get_dependencies_for_foreign_key(field)
                dependencies.append((app_label, model_name, None, True))
                self.add_operation(app_label, operations.AddField(model_name=model_name, name=name, field=field), dependencies=list(set(dependencies)))

            related_dependencies = [ (app_label, model_name, name, True) for name, field in sorted(related_fields.items())
                                   ]
            related_dependencies.append((app_label, model_name, None, True))
            for index in indexes:
                self.add_operation(app_label, operations.AddIndex(model_name=model_name, index=index), dependencies=related_dependencies)

            if unique_together:
                self.add_operation(app_label, operations.AlterUniqueTogether(name=model_name, unique_together=unique_together), dependencies=related_dependencies)
            if index_together:
                self.add_operation(app_label, operations.AlterIndexTogether(name=model_name, index_together=index_together), dependencies=related_dependencies)
            if order_with_respect_to:
                self.add_operation(app_label, operations.AlterOrderWithRespectTo(name=model_name, order_with_respect_to=order_with_respect_to), dependencies=[
                 (
                  app_label, model_name, order_with_respect_to, True),
                 (
                  app_label, model_name, None, True)])
            if (
             app_label, model_name) in self.old_proxy_keys:
                for related_object in model_opts.related_objects:
                    self.add_operation(related_object.related_model._meta.app_label, operations.AlterField(model_name=related_object.related_model._meta.object_name, name=related_object.field.name, field=related_object.field), dependencies=[
                     (
                      app_label, model_name, None, True)])

        return

    def generate_created_proxies(self):
        """
        Makes CreateModel statements for proxy models.
        We use the same statements as that way there's less code duplication,
        but of course for proxy models we can skip all that pointless field
        stuff and just chuck out an operation.
        """
        added = set(self.new_proxy_keys) - set(self.old_proxy_keys)
        for app_label, model_name in sorted(added):
            model_state = self.to_state.models[(app_label, model_name)]
            assert model_state.options.get(b'proxy')
            dependencies = [
             (
              app_label, model_name, None, False)]
            for base in model_state.bases:
                if isinstance(base, six.string_types) and b'.' in base:
                    base_app_label, base_name = base.split(b'.', 1)
                    dependencies.append((base_app_label, base_name, None, True))

            self.add_operation(app_label, operations.CreateModel(name=model_state.name, fields=[], options=model_state.options, bases=model_state.bases, managers=model_state.managers), dependencies=dependencies)

        return

    def generate_deleted_models(self):
        """
        Find all deleted models (managed and unmanaged) and make delete
        operations for them as well as separate operations to delete any
        foreign key or M2M relationships (we'll optimize these back in later
        if we can).

        We also bring forward removal of any model options that refer to
        collections of fields - the inverse of generate_created_models().
        """
        new_keys = set(self.new_model_keys).union(self.new_unmanaged_keys)
        deleted_models = set(self.old_model_keys) - new_keys
        deleted_unmanaged_models = set(self.old_unmanaged_keys) - new_keys
        all_deleted_models = chain(sorted(deleted_models), sorted(deleted_unmanaged_models))
        for app_label, model_name in all_deleted_models:
            model_state = self.from_state.models[(app_label, model_name)]
            model = self.old_apps.get_model(app_label, model_name)
            if not model._meta.managed:
                continue
            related_fields = {}
            for field in model._meta.local_fields:
                if field.remote_field:
                    if field.remote_field.model:
                        related_fields[field.name] = field
                    if getattr(field.remote_field, b'through', None) and not field.remote_field.through._meta.auto_created:
                        related_fields[field.name] = field

            for field in model._meta.local_many_to_many:
                if field.remote_field.model:
                    related_fields[field.name] = field
                if getattr(field.remote_field, b'through', None) and not field.remote_field.through._meta.auto_created:
                    related_fields[field.name] = field

            unique_together = model_state.options.pop(b'unique_together', None)
            index_together = model_state.options.pop(b'index_together', None)
            if unique_together:
                self.add_operation(app_label, operations.AlterUniqueTogether(name=model_name, unique_together=None))
            if index_together:
                self.add_operation(app_label, operations.AlterIndexTogether(name=model_name, index_together=None))
            for name, field in sorted(related_fields.items()):
                self.add_operation(app_label, operations.RemoveField(model_name=model_name, name=name))

            dependencies = []
            for related_object in model._meta.related_objects:
                related_object_app_label = related_object.related_model._meta.app_label
                object_name = related_object.related_model._meta.object_name
                field_name = related_object.field.name
                dependencies.append((related_object_app_label, object_name, field_name, False))
                if not related_object.many_to_many:
                    dependencies.append((related_object_app_label, object_name, field_name, b'alter'))

            for name, field in sorted(related_fields.items()):
                dependencies.append((app_label, model_name, name, False))

            through_user = self.through_users.get((app_label, model_state.name_lower))
            if through_user:
                dependencies.append((through_user[0], through_user[1], through_user[2], False))
            self.add_operation(app_label, operations.DeleteModel(name=model_state.name), dependencies=list(set(dependencies)))

        return

    def generate_deleted_proxies(self):
        """
        Makes DeleteModel statements for proxy models.
        """
        deleted = set(self.old_proxy_keys) - set(self.new_proxy_keys)
        for app_label, model_name in sorted(deleted):
            model_state = self.from_state.models[(app_label, model_name)]
            assert model_state.options.get(b'proxy')
            self.add_operation(app_label, operations.DeleteModel(name=model_state.name))

    def generate_renamed_fields(self):
        """
        Works out renamed fields
        """
        self.renamed_fields = {}
        for app_label, model_name, field_name in sorted(self.new_field_keys - self.old_field_keys):
            old_model_name = self.renamed_models.get((app_label, model_name), model_name)
            old_model_state = self.from_state.models[(app_label, old_model_name)]
            field = self.new_apps.get_model(app_label, model_name)._meta.get_field(field_name)
            field_dec = self.deep_deconstruct(field)
            for rem_app_label, rem_model_name, rem_field_name in sorted(self.old_field_keys - self.new_field_keys):
                if rem_app_label == app_label and rem_model_name == model_name:
                    old_field_dec = self.deep_deconstruct(old_model_state.get_field_by_name(rem_field_name))
                    if field.remote_field and field.remote_field.model and b'to' in old_field_dec[2]:
                        old_rel_to = old_field_dec[2][b'to']
                        if old_rel_to in self.renamed_models_rel:
                            old_field_dec[2][b'to'] = self.renamed_models_rel[old_rel_to]
                    if old_field_dec == field_dec:
                        if self.questioner.ask_rename(model_name, rem_field_name, field_name, field):
                            self.add_operation(app_label, operations.RenameField(model_name=model_name, old_name=rem_field_name, new_name=field_name))
                            self.old_field_keys.remove((rem_app_label, rem_model_name, rem_field_name))
                            self.old_field_keys.add((app_label, model_name, field_name))
                            self.renamed_fields[(app_label, model_name, field_name)] = rem_field_name
                            break

    def generate_added_fields(self):
        """
        Fields that have been added
        """
        for app_label, model_name, field_name in sorted(self.new_field_keys - self.old_field_keys):
            self._generate_added_field(app_label, model_name, field_name)

    def _generate_added_field(self, app_label, model_name, field_name):
        field = self.new_apps.get_model(app_label, model_name)._meta.get_field(field_name)
        dependencies = []
        if field.remote_field and field.remote_field.model:
            dependencies.extend(self._get_dependencies_for_foreign_key(field))
        preserve_default = True
        time_fields = (models.DateField, models.DateTimeField, models.TimeField)
        if not field.null and not field.has_default() and not field.many_to_many and not (field.blank and field.empty_strings_allowed) and not (isinstance(field, time_fields) and field.auto_now):
            field = field.clone()
            if isinstance(field, time_fields) and field.auto_now_add:
                field.default = self.questioner.ask_auto_now_add_addition(field_name, model_name)
            else:
                field.default = self.questioner.ask_not_null_addition(field_name, model_name)
            preserve_default = False
        self.add_operation(app_label, operations.AddField(model_name=model_name, name=field_name, field=field, preserve_default=preserve_default), dependencies=dependencies)

    def generate_removed_fields(self):
        """
        Fields that have been removed.
        """
        for app_label, model_name, field_name in sorted(self.old_field_keys - self.new_field_keys):
            self._generate_removed_field(app_label, model_name, field_name)

    def _generate_removed_field(self, app_label, model_name, field_name):
        self.add_operation(app_label, operations.RemoveField(model_name=model_name, name=field_name), dependencies=[
         (
          app_label, model_name, field_name, b'order_wrt_unset'),
         (
          app_label, model_name, field_name, b'foo_together_change')])

    def generate_altered_fields(self):
        """
        Fields that have been altered.
        """
        for app_label, model_name, field_name in sorted(self.old_field_keys.intersection(self.new_field_keys)):
            old_model_name = self.renamed_models.get((app_label, model_name), model_name)
            old_field_name = self.renamed_fields.get((app_label, model_name, field_name), field_name)
            old_field = self.old_apps.get_model(app_label, old_model_name)._meta.get_field(old_field_name)
            new_field = self.new_apps.get_model(app_label, model_name)._meta.get_field(field_name)
            if hasattr(new_field, b'remote_field') and getattr(new_field.remote_field, b'model', None):
                rename_key = (new_field.remote_field.model._meta.app_label,
                 new_field.remote_field.model._meta.model_name)
                if rename_key in self.renamed_models:
                    new_field.remote_field.model = old_field.remote_field.model
            if hasattr(new_field, b'remote_field') and getattr(new_field.remote_field, b'through', None):
                rename_key = (new_field.remote_field.through._meta.app_label,
                 new_field.remote_field.through._meta.model_name)
                if rename_key in self.renamed_models:
                    new_field.remote_field.through = old_field.remote_field.through
            old_field_dec = self.deep_deconstruct(old_field)
            new_field_dec = self.deep_deconstruct(new_field)
            if old_field_dec != new_field_dec:
                both_m2m = old_field.many_to_many and new_field.many_to_many
                neither_m2m = not old_field.many_to_many and not new_field.many_to_many
                if both_m2m or neither_m2m:
                    preserve_default = True
                    if old_field.null and not new_field.null and not new_field.has_default() and not new_field.many_to_many:
                        field = new_field.clone()
                        new_default = self.questioner.ask_not_null_alteration(field_name, model_name)
                        if new_default is not models.NOT_PROVIDED:
                            field.default = new_default
                            preserve_default = False
                    else:
                        field = new_field
                    self.add_operation(app_label, operations.AlterField(model_name=model_name, name=field_name, field=field, preserve_default=preserve_default))
                else:
                    self._generate_removed_field(app_label, model_name, field_name)
                    self._generate_added_field(app_label, model_name, field_name)

        return

    def create_altered_indexes(self):
        option_name = operations.AddIndex.option_name
        for app_label, model_name in sorted(self.kept_model_keys):
            old_model_name = self.renamed_models.get((app_label, model_name), model_name)
            old_model_state = self.from_state.models[(app_label, old_model_name)]
            new_model_state = self.to_state.models[(app_label, model_name)]
            old_indexes = old_model_state.options[option_name]
            new_indexes = new_model_state.options[option_name]
            add_idx = [ idx for idx in new_indexes if idx not in old_indexes ]
            rem_idx = [ idx for idx in old_indexes if idx not in new_indexes ]
            self.altered_indexes.update({(app_label, model_name): {b'added_indexes': add_idx, 
                                         b'removed_indexes': rem_idx}})

    def generate_added_indexes(self):
        for (app_label, model_name), alt_indexes in self.altered_indexes.items():
            for index in alt_indexes[b'added_indexes']:
                self.add_operation(app_label, operations.AddIndex(model_name=model_name, index=index))

    def generate_removed_indexes(self):
        for (app_label, model_name), alt_indexes in self.altered_indexes.items():
            for index in alt_indexes[b'removed_indexes']:
                self.add_operation(app_label, operations.RemoveIndex(model_name=model_name, name=index.name))

    def _get_dependencies_for_foreign_key(self, field):
        swappable_setting = getattr(field, b'swappable_setting', None)
        if swappable_setting is not None:
            dep_app_label = b'__setting__'
            dep_object_name = swappable_setting
        else:
            dep_app_label = field.remote_field.model._meta.app_label
            dep_object_name = field.remote_field.model._meta.object_name
        dependencies = [
         (
          dep_app_label, dep_object_name, None, True)]
        if getattr(field.remote_field, b'through', None) and not field.remote_field.through._meta.auto_created:
            dependencies.append((
             field.remote_field.through._meta.app_label,
             field.remote_field.through._meta.object_name,
             None,
             True))
        return dependencies

    def _generate_altered_foo_together(self, operation):
        option_name = operation.option_name
        for app_label, model_name in sorted(self.kept_model_keys):
            old_model_name = self.renamed_models.get((app_label, model_name), model_name)
            old_model_state = self.from_state.models[(app_label, old_model_name)]
            new_model_state = self.to_state.models[(app_label, model_name)]
            old_value = old_model_state.options.get(option_name) or set()
            if old_value:
                old_value = {tuple(self.renamed_fields.get((app_label, model_name, n), n) for n in unique) for unique in old_value}
            new_value = new_model_state.options.get(option_name) or set()
            if new_value:
                new_value = set(new_value)
            if old_value != new_value:
                dependencies = []
                for foo_togethers in new_value:
                    for field_name in foo_togethers:
                        field = self.new_apps.get_model(app_label, model_name)._meta.get_field(field_name)
                        if field.remote_field and field.remote_field.model:
                            dependencies.extend(self._get_dependencies_for_foreign_key(field))

                self.add_operation(app_label, operation(name=model_name, **{option_name: new_value}), dependencies=dependencies)

    def generate_altered_unique_together(self):
        self._generate_altered_foo_together(operations.AlterUniqueTogether)

    def generate_altered_index_together(self):
        self._generate_altered_foo_together(operations.AlterIndexTogether)

    def generate_altered_db_table(self):
        models_to_check = self.kept_model_keys.union(self.kept_proxy_keys).union(self.kept_unmanaged_keys)
        for app_label, model_name in sorted(models_to_check):
            old_model_name = self.renamed_models.get((app_label, model_name), model_name)
            old_model_state = self.from_state.models[(app_label, old_model_name)]
            new_model_state = self.to_state.models[(app_label, model_name)]
            old_db_table_name = old_model_state.options.get(b'db_table')
            new_db_table_name = new_model_state.options.get(b'db_table')
            if old_db_table_name != new_db_table_name:
                self.add_operation(app_label, operations.AlterModelTable(name=model_name, table=new_db_table_name))

    def generate_altered_options(self):
        """
        Works out if any non-schema-affecting options have changed and
        makes an operation to represent them in state changes (in case Python
        code in migrations needs them)
        """
        models_to_check = self.kept_model_keys.union(self.kept_proxy_keys).union(self.kept_unmanaged_keys).union(set(self.old_unmanaged_keys).intersection(self.new_model_keys)).union(set(self.old_model_keys).intersection(self.new_unmanaged_keys))
        for app_label, model_name in sorted(models_to_check):
            old_model_name = self.renamed_models.get((app_label, model_name), model_name)
            old_model_state = self.from_state.models[(app_label, old_model_name)]
            new_model_state = self.to_state.models[(app_label, model_name)]
            old_options = dict(option for option in old_model_state.options.items() if option[0] in AlterModelOptions.ALTER_OPTION_KEYS)
            new_options = dict(option for option in new_model_state.options.items() if option[0] in AlterModelOptions.ALTER_OPTION_KEYS)
            if old_options != new_options:
                self.add_operation(app_label, operations.AlterModelOptions(name=model_name, options=new_options))

    def generate_altered_order_with_respect_to(self):
        for app_label, model_name in sorted(self.kept_model_keys):
            old_model_name = self.renamed_models.get((app_label, model_name), model_name)
            old_model_state = self.from_state.models[(app_label, old_model_name)]
            new_model_state = self.to_state.models[(app_label, model_name)]
            if old_model_state.options.get(b'order_with_respect_to') != new_model_state.options.get(b'order_with_respect_to'):
                dependencies = []
                if new_model_state.options.get(b'order_with_respect_to'):
                    dependencies.append((
                     app_label,
                     model_name,
                     new_model_state.options[b'order_with_respect_to'],
                     True))
                self.add_operation(app_label, operations.AlterOrderWithRespectTo(name=model_name, order_with_respect_to=new_model_state.options.get(b'order_with_respect_to')), dependencies=dependencies)

    def generate_altered_managers(self):
        for app_label, model_name in sorted(self.kept_model_keys):
            old_model_name = self.renamed_models.get((app_label, model_name), model_name)
            old_model_state = self.from_state.models[(app_label, old_model_name)]
            new_model_state = self.to_state.models[(app_label, model_name)]
            if old_model_state.managers != new_model_state.managers:
                self.add_operation(app_label, operations.AlterModelManagers(name=model_name, managers=new_model_state.managers))

    def arrange_for_graph(self, changes, graph, migration_name=None):
        """
        Takes in a result from changes() and a MigrationGraph,
        and fixes the names and dependencies of the changes so they
        extend the graph from the leaf nodes for each app.
        """
        leaves = graph.leaf_nodes()
        name_map = {}
        for app_label, migrations in list(changes.items()):
            if not migrations:
                continue
            app_leaf = None
            for leaf in leaves:
                if leaf[0] == app_label:
                    app_leaf = leaf
                    break

            if app_leaf is None and not self.questioner.ask_initial(app_label):
                for migration in migrations:
                    name_map[(app_label, migration.name)] = (
                     app_label, b'__first__')

                del changes[app_label]
                continue
            if app_leaf is None:
                next_number = 1
            else:
                next_number = (self.parse_number(app_leaf[1]) or 0) + 1
            for i, migration in enumerate(migrations):
                if i == 0 and app_leaf:
                    migration.dependencies.append(app_leaf)
                if i == 0 and not app_leaf:
                    new_name = b'0001_%s' % migration_name if migration_name else b'0001_initial'
                else:
                    new_name = b'%04i_%s' % (
                     next_number,
                     migration_name or self.suggest_name(migration.operations)[:100])
                name_map[(app_label, migration.name)] = (app_label, new_name)
                next_number += 1
                migration.name = new_name

        for app_label, migrations in changes.items():
            for migration in migrations:
                migration.dependencies = [ name_map.get(d, d) for d in migration.dependencies ]

        return changes

    def _trim_to_apps(self, changes, app_labels):
        """
        Takes changes from arrange_for_graph and set of app labels and
        returns a modified set of changes which trims out as many migrations
        that are not in app_labels as possible.
        Note that some other migrations may still be present, as they may be
        required dependencies.
        """
        app_dependencies = {}
        for app_label, migrations in changes.items():
            for migration in migrations:
                for dep_app_label, name in migration.dependencies:
                    app_dependencies.setdefault(app_label, set()).add(dep_app_label)

        required_apps = set(app_labels)
        old_required_apps = None
        while old_required_apps != required_apps:
            old_required_apps = set(required_apps)
            for app_label in list(required_apps):
                required_apps.update(app_dependencies.get(app_label, set()))

        for app_label in list(changes.keys()):
            if app_label not in required_apps:
                del changes[app_label]

        return changes

    @classmethod
    def suggest_name(cls, ops):
        """
        Given a set of operations, suggests a name for the migration
        they might represent. Names are not guaranteed to be unique,
        but we put some effort in to the fallback name to avoid VCS conflicts
        if we can.
        """
        if len(ops) == 1:
            if isinstance(ops[0], operations.CreateModel):
                return ops[0].name_lower
            if isinstance(ops[0], operations.DeleteModel):
                return b'delete_%s' % ops[0].name_lower
            if isinstance(ops[0], operations.AddField):
                return b'%s_%s' % (ops[0].model_name_lower, ops[0].name_lower)
            if isinstance(ops[0], operations.RemoveField):
                return b'remove_%s_%s' % (ops[0].model_name_lower, ops[0].name_lower)
        elif len(ops) > 1:
            if all(isinstance(o, operations.CreateModel) for o in ops):
                return (b'_').join(sorted(o.name_lower for o in ops))
        return b'auto_%s' % get_migration_name_timestamp()

    @classmethod
    def parse_number(cls, name):
        """
        Given a migration name, tries to extract a number from the
        beginning of it. If no number found, returns None.
        """
        match = re.match(b'^\\d+', name)
        if match:
            return int(match.group())
        else:
            return
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/management/commands/migrate.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import time
from collections import OrderedDict
from importlib import import_module
from django.apps import apps
from django.core.checks import Tags, run_checks
from django.core.management.base import BaseCommand, CommandError
from django.core.management.sql import emit_post_migrate_signal, emit_pre_migrate_signal
from django.db import DEFAULT_DB_ALIAS, connections, router
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.loader import AmbiguityError
from django.db.migrations.state import ModelState, ProjectState
from django.utils.module_loading import module_has_submodule

class Command(BaseCommand):
    help = b'Updates database schema. Manages both apps with migrations and those without.'

    def add_arguments(self, parser):
        parser.add_argument(b'app_label', nargs=b'?', help=b'App label of an application to synchronize the state.')
        parser.add_argument(b'migration_name', nargs=b'?', help=b'Database state will be brought to the state after that migration. Use the name "zero" to unapply all migrations.')
        parser.add_argument(b'--noinput', b'--no-input', action=b'store_false', dest=b'interactive', default=True, help=b'Tells Django to NOT prompt the user for input of any kind.')
        parser.add_argument(b'--database', action=b'store', dest=b'database', default=DEFAULT_DB_ALIAS, help=b'Nominates a database to synchronize. Defaults to the "default" database.')
        parser.add_argument(b'--fake', action=b'store_true', dest=b'fake', default=False, help=b'Mark migrations as run without actually running them.')
        parser.add_argument(b'--fake-initial', action=b'store_true', dest=b'fake_initial', default=False, help=b'Detect if tables already exist and fake-apply initial migrations if so. Make sure that the current database schema matches your initial migration before using this flag. Django will only check for an existing table name.')
        parser.add_argument(b'--run-syncdb', action=b'store_true', dest=b'run_syncdb', help=b'Creates tables for apps without migrations.')

    def _run_checks(self, **kwargs):
        issues = run_checks(tags=[Tags.database])
        issues.extend(super(Command, self)._run_checks(**kwargs))
        return issues

    def handle(self, *args, **options):
        self.verbosity = options[b'verbosity']
        self.interactive = options[b'interactive']
        for app_config in apps.get_app_configs():
            if module_has_submodule(app_config.module, b'management'):
                import_module(b'.management', app_config.name)

        db = options[b'database']
        connection = connections[db]
        connection.prepare_database()
        executor = MigrationExecutor(connection, self.migration_progress_callback)
        executor.loader.check_consistent_history(connection)
        conflicts = executor.loader.detect_conflicts()
        if conflicts:
            name_str = (b'; ').join(b'%s in %s' % ((b', ').join(names), app) for app, names in conflicts.items())
            raise CommandError(b"Conflicting migrations detected; multiple leaf nodes in the migration graph: (%s).\nTo fix them run 'python manage.py makemigrations --merge'" % name_str)
        target_app_labels_only = True
        if options[b'app_label'] and options[b'migration_name']:
            app_label, migration_name = options[b'app_label'], options[b'migration_name']
            if app_label not in executor.loader.migrated_apps:
                raise CommandError(b"App '%s' does not have migrations." % app_label)
            if migration_name == b'zero':
                targets = [
                 (
                  app_label, None)]
            else:
                try:
                    migration = executor.loader.get_migration_by_prefix(app_label, migration_name)
                except AmbiguityError:
                    raise CommandError(b"More than one migration matches '%s' in app '%s'. Please be more specific." % (
                     migration_name, app_label))
                except KeyError:
                    raise CommandError(b"Cannot find a migration matching '%s' from app '%s'." % (
                     migration_name, app_label))

                targets = [
                 (
                  app_label, migration.name)]
            target_app_labels_only = False
        elif options[b'app_label']:
            app_label = options[b'app_label']
            if app_label not in executor.loader.migrated_apps:
                raise CommandError(b"App '%s' does not have migrations." % app_label)
            targets = [ key for key in executor.loader.graph.leaf_nodes() if key[0] == app_label ]
        else:
            targets = executor.loader.graph.leaf_nodes()
        plan = executor.migration_plan(targets)
        run_syncdb = options[b'run_syncdb'] and executor.loader.unmigrated_apps
        if self.verbosity >= 1:
            self.stdout.write(self.style.MIGRATE_HEADING(b'Operations to perform:'))
            if run_syncdb:
                self.stdout.write(self.style.MIGRATE_LABEL(b'  Synchronize unmigrated apps: ') + (b', ').join(sorted(executor.loader.unmigrated_apps)))
            if target_app_labels_only:
                self.stdout.write(self.style.MIGRATE_LABEL(b'  Apply all migrations: ') + ((b', ').join(sorted(set(a for a, n in targets))) or b'(none)'))
            elif targets[0][1] is None:
                self.stdout.write(self.style.MIGRATE_LABEL(b'  Unapply all migrations: ') + b'%s' % (targets[0][0],))
            else:
                self.stdout.write(self.style.MIGRATE_LABEL(b'  Target specific migration: ') + b'%s, from %s' % (
                 targets[0][1], targets[0][0]))
        pre_migrate_state = executor._create_project_state(with_applied_migrations=True)
        pre_migrate_apps = pre_migrate_state.apps
        emit_pre_migrate_signal(self.verbosity, self.interactive, connection.alias, apps=pre_migrate_apps, plan=plan)
        if run_syncdb:
            if self.verbosity >= 1:
                self.stdout.write(self.style.MIGRATE_HEADING(b'Synchronizing apps without migrations:'))
            self.sync_apps(connection, executor.loader.unmigrated_apps)
        if self.verbosity >= 1:
            self.stdout.write(self.style.MIGRATE_HEADING(b'Running migrations:'))
        if not plan:
            if self.verbosity >= 1:
                self.stdout.write(b'  No migrations to apply.')
                autodetector = MigrationAutodetector(executor.loader.project_state(), ProjectState.from_apps(apps))
                changes = autodetector.changes(graph=executor.loader.graph)
                if changes:
                    self.stdout.write(self.style.NOTICE(b"  Your models have changes that are not yet reflected in a migration, and so won't be applied."))
                    self.stdout.write(self.style.NOTICE(b"  Run 'manage.py makemigrations' to make new migrations, and then re-run 'manage.py migrate' to apply them."))
            fake = False
            fake_initial = False
        else:
            fake = options[b'fake']
            fake_initial = options[b'fake_initial']
        post_migrate_state = executor.migrate(targets, plan=plan, state=pre_migrate_state.clone(), fake=fake, fake_initial=fake_initial)
        post_migrate_state.clear_delayed_apps_cache()
        post_migrate_apps = post_migrate_state.apps
        with post_migrate_apps.bulk_update():
            model_keys = []
            for model_state in post_migrate_apps.real_models:
                model_key = (
                 model_state.app_label, model_state.name_lower)
                model_keys.append(model_key)
                post_migrate_apps.unregister_model(*model_key)

        post_migrate_apps.render_multiple([ ModelState.from_model(apps.get_model(*model)) for model in model_keys ])
        emit_post_migrate_signal(self.verbosity, self.interactive, connection.alias, apps=post_migrate_apps, plan=plan)
        return

    def migration_progress_callback(self, action, migration=None, fake=False):
        if self.verbosity >= 1:
            compute_time = self.verbosity > 1
            if action == b'apply_start':
                if compute_time:
                    self.start = time.time()
                self.stdout.write(b'  Applying %s...' % migration, ending=b'')
                self.stdout.flush()
            elif action == b'apply_success':
                elapsed = b' (%.3fs)' % (time.time() - self.start) if compute_time else b''
                if fake:
                    self.stdout.write(self.style.SUCCESS(b' FAKED' + elapsed))
                else:
                    self.stdout.write(self.style.SUCCESS(b' OK' + elapsed))
            elif action == b'unapply_start':
                if compute_time:
                    self.start = time.time()
                self.stdout.write(b'  Unapplying %s...' % migration, ending=b'')
                self.stdout.flush()
            elif action == b'unapply_success':
                elapsed = b' (%.3fs)' % (time.time() - self.start) if compute_time else b''
                if fake:
                    self.stdout.write(self.style.SUCCESS(b' FAKED' + elapsed))
                else:
                    self.stdout.write(self.style.SUCCESS(b' OK' + elapsed))
            elif action == b'render_start':
                if compute_time:
                    self.start = time.time()
                self.stdout.write(b'  Rendering model states...', ending=b'')
                self.stdout.flush()
            elif action == b'render_success':
                elapsed = b' (%.3fs)' % (time.time() - self.start) if compute_time else b''
                self.stdout.write(self.style.SUCCESS(b' DONE' + elapsed))

    def sync_apps(self, connection, app_labels):
        """Run the old syncdb-style operation on a list of app_labels."""
        with connection.cursor() as (cursor):
            tables = connection.introspection.table_names(cursor)
        all_models = [ (app_config.label, router.get_migratable_models(app_config, connection.alias, include_auto_created=False)) for app_config in apps.get_app_configs() if app_config.models_module is not None and app_config.label in app_labels
                     ]

        def model_installed(model):
            opts = model._meta
            converter = connection.introspection.table_name_converter
            return not (converter(opts.db_table) in tables or opts.auto_created and converter(opts.auto_created._meta.db_table) in tables)

        manifest = OrderedDict((app_name, list(filter(model_installed, model_list))) for app_name, model_list in all_models)
        if self.verbosity >= 1:
            self.stdout.write(b'  Creating tables...\n')
        with connection.schema_editor() as (editor):
            for app_name, model_list in manifest.items():
                for model in model_list:
                    if not model._meta.can_migrate(connection):
                        continue
                    if self.verbosity >= 3:
                        self.stdout.write(b'    Processing %s.%s model\n' % (app_name, model._meta.object_name))
                    if self.verbosity >= 1:
                        self.stdout.write(b'    Creating table %s\n' % model._meta.db_table)
                    editor.create_model(model)

            if self.verbosity >= 1:
                self.stdout.write(b'    Running deferred SQL...\n')
        return
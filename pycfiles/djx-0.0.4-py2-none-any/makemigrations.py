# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/management/commands/makemigrations.py
# Compiled at: 2019-02-14 00:35:17
import io, os, sys, warnings
from itertools import takewhile
from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS, connections, router
from django.db.migrations import Migration
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.questioner import InteractiveMigrationQuestioner, MigrationQuestioner, NonInteractiveMigrationQuestioner
from django.db.migrations.state import ProjectState
from django.db.migrations.utils import get_migration_name_timestamp
from django.db.migrations.writer import MigrationWriter
from django.utils.deprecation import RemovedInDjango20Warning
from django.utils.six import iteritems
from django.utils.six.moves import zip

class Command(BaseCommand):
    help = 'Creates new migration(s) for apps.'

    def add_arguments(self, parser):
        parser.add_argument('args', metavar='app_label', nargs='*', help='Specify the app label(s) to create migrations for.')
        parser.add_argument('--dry-run', action='store_true', dest='dry_run', default=False, help="Just show what migrations would be made; don't actually write them.")
        parser.add_argument('--merge', action='store_true', dest='merge', default=False, help='Enable fixing of migration conflicts.')
        parser.add_argument('--empty', action='store_true', dest='empty', default=False, help='Create an empty migration.')
        parser.add_argument('--noinput', '--no-input', action='store_false', dest='interactive', default=True, help='Tells Django to NOT prompt the user for input of any kind.')
        parser.add_argument('-n', '--name', action='store', dest='name', default=None, help='Use this name for migration file(s).')
        parser.add_argument('-e', '--exit', action='store_true', dest='exit_code', default=False, help='Exit with error code 1 if no changes needing migrations are found. Deprecated, use the --check option instead.')
        parser.add_argument('--check', action='store_true', dest='check_changes', help='Exit with a non-zero status if model changes are missing migrations.')
        return

    def handle(self, *app_labels, **options):
        self.verbosity = options['verbosity']
        self.interactive = options['interactive']
        self.dry_run = options['dry_run']
        self.merge = options['merge']
        self.empty = options['empty']
        self.migration_name = options['name']
        self.exit_code = options['exit_code']
        check_changes = options['check_changes']
        if self.exit_code:
            warnings.warn('The --exit option is deprecated in favor of the --check option.', RemovedInDjango20Warning)
        app_labels = set(app_labels)
        bad_app_labels = set()
        for app_label in app_labels:
            try:
                apps.get_app_config(app_label)
            except LookupError:
                bad_app_labels.add(app_label)

        if bad_app_labels:
            for app_label in bad_app_labels:
                self.stderr.write("App '%s' could not be found. Is it in INSTALLED_APPS?" % app_label)

            sys.exit(2)
        loader = MigrationLoader(None, ignore_no_migrations=True)
        consistency_check_labels = set(config.label for config in apps.get_app_configs())
        aliases_to_check = connections if settings.DATABASE_ROUTERS else [DEFAULT_DB_ALIAS]
        for alias in sorted(aliases_to_check):
            connection = connections[alias]
            if connection.settings_dict['ENGINE'] != 'django.db.backends.dummy' and any(router.allow_migrate(connection.alias, app_label, model_name=model._meta.object_name) for app_label in consistency_check_labels for model in apps.get_app_config(app_label).get_models()):
                loader.check_consistent_history(connection)

        conflicts = loader.detect_conflicts()
        if app_labels:
            conflicts = {app_label:conflict for app_label, conflict in iteritems(conflicts) if app_label in app_labels}
        if conflicts and not self.merge:
            name_str = ('; ').join('%s in %s' % ((', ').join(names), app) for app, names in conflicts.items())
            raise CommandError("Conflicting migrations detected; multiple leaf nodes in the migration graph: (%s).\nTo fix them run 'python manage.py makemigrations --merge'" % name_str)
        if self.merge and not conflicts:
            self.stdout.write('No conflicts detected to merge.')
            return
        else:
            if self.merge and conflicts:
                return self.handle_merge(loader, conflicts)
            if self.interactive:
                questioner = InteractiveMigrationQuestioner(specified_apps=app_labels, dry_run=self.dry_run)
            else:
                questioner = NonInteractiveMigrationQuestioner(specified_apps=app_labels, dry_run=self.dry_run)
            autodetector = MigrationAutodetector(loader.project_state(), ProjectState.from_apps(apps), questioner)
            if self.empty:
                if not app_labels:
                    raise CommandError('You must supply at least one app label when using --empty.')
                changes = {app:[Migration('custom', app)] for app in app_labels}
                changes = autodetector.arrange_for_graph(changes=changes, graph=loader.graph, migration_name=self.migration_name)
                self.write_migration_files(changes)
                return
            changes = autodetector.changes(graph=loader.graph, trim_to_apps=app_labels or None, convert_apps=app_labels or None, migration_name=self.migration_name)
            if not changes:
                if self.verbosity >= 1:
                    if len(app_labels) == 1:
                        self.stdout.write("No changes detected in app '%s'" % app_labels.pop())
                    elif len(app_labels) > 1:
                        self.stdout.write("No changes detected in apps '%s'" % ("', '").join(app_labels))
                    else:
                        self.stdout.write('No changes detected')
                if self.exit_code:
                    sys.exit(1)
            else:
                self.write_migration_files(changes)
                if check_changes:
                    sys.exit(1)
            return

    def write_migration_files(self, changes):
        """
        Takes a changes dict and writes them out as migration files.
        """
        directory_created = {}
        for app_label, app_migrations in changes.items():
            if self.verbosity >= 1:
                self.stdout.write(self.style.MIGRATE_HEADING("Migrations for '%s':" % app_label) + '\n')
            for migration in app_migrations:
                writer = MigrationWriter(migration)
                if self.verbosity >= 1:
                    try:
                        migration_string = os.path.relpath(writer.path)
                    except ValueError:
                        migration_string = writer.path

                    if migration_string.startswith('..'):
                        migration_string = writer.path
                    self.stdout.write('  %s\n' % (self.style.MIGRATE_LABEL(migration_string),))
                    for operation in migration.operations:
                        self.stdout.write('    - %s\n' % operation.describe())

                if not self.dry_run:
                    migrations_directory = os.path.dirname(writer.path)
                    if not directory_created.get(app_label):
                        if not os.path.isdir(migrations_directory):
                            os.mkdir(migrations_directory)
                        init_path = os.path.join(migrations_directory, '__init__.py')
                        if not os.path.isfile(init_path):
                            open(init_path, 'w').close()
                        directory_created[app_label] = True
                    migration_string = writer.as_string()
                    with io.open(writer.path, 'w', encoding='utf-8') as (fh):
                        fh.write(migration_string)
                elif self.verbosity == 3:
                    self.stdout.write(self.style.MIGRATE_HEADING("Full migrations file '%s':" % writer.filename) + '\n')
                    self.stdout.write('%s\n' % writer.as_string())

    def handle_merge(self, loader, conflicts):
        """
        Handles merging together conflicted migrations interactively,
        if it's safe; otherwise, advises on how to fix it.
        """
        if self.interactive:
            questioner = InteractiveMigrationQuestioner()
        else:
            questioner = MigrationQuestioner(defaults={'ask_merge': True})
        for app_label, migration_names in conflicts.items():
            merge_migrations = []
            for migration_name in migration_names:
                migration = loader.get_migration(app_label, migration_name)
                migration.ancestry = [ mig for mig in loader.graph.forwards_plan((app_label, migration_name)) if mig[0] == migration.app_label
                                     ]
                merge_migrations.append(migration)

            def all_items_equal(seq):
                return all(item == seq[0] for item in seq[1:])

            merge_migrations_generations = zip(*[ m.ancestry for m in merge_migrations ])
            common_ancestor_count = sum(1 for common_ancestor_generation in takewhile(all_items_equal, merge_migrations_generations))
            if not common_ancestor_count:
                raise ValueError('Could not find common ancestor of %s' % migration_names)
            for migration in merge_migrations:
                migration.branch = migration.ancestry[common_ancestor_count:]
                migrations_ops = (loader.get_migration(node_app, node_name).operations for node_app, node_name in migration.branch)
                migration.merged_operations = sum(migrations_ops, [])

            if self.verbosity > 0:
                self.stdout.write(self.style.MIGRATE_HEADING('Merging %s' % app_label))
                for migration in merge_migrations:
                    self.stdout.write(self.style.MIGRATE_LABEL('  Branch %s' % migration.name))
                    for operation in migration.merged_operations:
                        self.stdout.write('    - %s\n' % operation.describe())

            if questioner.ask_merge(app_label):
                numbers = [ MigrationAutodetector.parse_number(migration.name) for migration in merge_migrations
                          ]
                try:
                    biggest_number = max(x for x in numbers if x is not None)
                except ValueError:
                    biggest_number = 1

                subclass = type('Migration', (Migration,), {'dependencies': [ (app_label, migration.name) for migration in merge_migrations ]})
                migration_name = '%04i_%s' % (
                 biggest_number + 1,
                 self.migration_name or 'merge_%s' % get_migration_name_timestamp())
                new_migration = subclass(migration_name, app_label)
                writer = MigrationWriter(new_migration)
                if not self.dry_run:
                    with io.open(writer.path, 'w', encoding='utf-8') as (fh):
                        fh.write(writer.as_string())
                    if self.verbosity > 0:
                        self.stdout.write('\nCreated new merge migration %s' % writer.path)
                elif self.verbosity == 3:
                    self.stdout.write(self.style.MIGRATE_HEADING("Full merge migrations file '%s':" % writer.filename) + '\n')
                    self.stdout.write('%s\n' % writer.as_string())
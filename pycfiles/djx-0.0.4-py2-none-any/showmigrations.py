# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/management/commands/showmigrations.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.loader import MigrationLoader

class Command(BaseCommand):
    help = b'Shows all available migrations for the current project'

    def add_arguments(self, parser):
        parser.add_argument(b'app_label', nargs=b'*', help=b'App labels of applications to limit the output to.')
        parser.add_argument(b'--database', action=b'store', dest=b'database', default=DEFAULT_DB_ALIAS, help=b'Nominates a database to synchronize. Defaults to the "default" database.')
        formats = parser.add_mutually_exclusive_group()
        formats.add_argument(b'--list', b'-l', action=b'store_const', dest=b'format', const=b'list', help=b'Shows a list of all migrations and which are applied.')
        formats.add_argument(b'--plan', b'-p', action=b'store_const', dest=b'format', const=b'plan', help=b'Shows all migrations in the order they will be applied. With a verbosity level of 2 or above all direct migration dependencies and reverse dependencies (run_before) will be included.')
        parser.set_defaults(format=b'list')

    def handle(self, *args, **options):
        self.verbosity = options[b'verbosity']
        db = options[b'database']
        connection = connections[db]
        if options[b'format'] == b'plan':
            return self.show_plan(connection, options[b'app_label'])
        else:
            return self.show_list(connection, options[b'app_label'])

    def _validate_app_names(self, loader, app_names):
        invalid_apps = []
        for app_name in app_names:
            if app_name not in loader.migrated_apps:
                invalid_apps.append(app_name)

        if invalid_apps:
            raise CommandError(b'No migrations present for: %s' % (b', ').join(sorted(invalid_apps)))

    def show_list(self, connection, app_names=None):
        """
        Shows a list of all migrations on the system, or only those of
        some named apps.
        """
        loader = MigrationLoader(connection, ignore_no_migrations=True)
        graph = loader.graph
        if app_names:
            self._validate_app_names(loader, app_names)
        else:
            app_names = sorted(loader.migrated_apps)
        for app_name in app_names:
            self.stdout.write(app_name, self.style.MIGRATE_LABEL)
            shown = set()
            for node in graph.leaf_nodes(app_name):
                for plan_node in graph.forwards_plan(node):
                    if plan_node not in shown and plan_node[0] == app_name:
                        title = plan_node[1]
                        if graph.nodes[plan_node].replaces:
                            title += b' (%s squashed migrations)' % len(graph.nodes[plan_node].replaces)
                        if plan_node in loader.applied_migrations:
                            self.stdout.write(b' [X] %s' % title)
                        else:
                            self.stdout.write(b' [ ] %s' % title)
                        shown.add(plan_node)

            if not shown:
                self.stdout.write(b' (no migrations)', self.style.ERROR)

    def show_plan(self, connection, app_names=None):
        """
        Shows all known migrations (or only those of the specified app_names)
        in the order they will be applied.
        """
        loader = MigrationLoader(connection)
        graph = loader.graph
        if app_names:
            self._validate_app_names(loader, app_names)
            targets = [ key for key in graph.leaf_nodes() if key[0] in app_names ]
        else:
            targets = graph.leaf_nodes()
        plan = []
        seen = set()
        for target in targets:
            for migration in graph.forwards_plan(target):
                if migration not in seen:
                    node = graph.node_map[migration]
                    plan.append(node)
                    seen.add(migration)

        def print_deps(node):
            out = []
            for parent in sorted(node.parents):
                out.append(b'%s.%s' % parent.key)

            if out:
                return b' ... (%s)' % (b', ').join(out)
            return b''

        for node in plan:
            deps = b''
            if self.verbosity >= 2:
                deps = print_deps(node)
            if node.key in loader.applied_migrations:
                self.stdout.write(b'[X]  %s.%s%s' % (node.key[0], node.key[1], deps))
            else:
                self.stdout.write(b'[ ]  %s.%s%s' % (node.key[0], node.key[1], deps))
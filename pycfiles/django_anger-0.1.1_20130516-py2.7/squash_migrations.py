# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django_anger/squash_migrations.py
# Compiled at: 2013-05-13 19:36:08
"""
Squash the initial migrations for multiple apps into a single combined
migration, avoiding potential issues with circular dependencies. See
ResettingMigrations.md for details.

Usage:
    # All apps in your Django project must have only an initial migration.
    # Say you want to save the squashed migration in app_alpha.
    squash_migrations app_alpha
"""
from StringIO import StringIO
import os, shutil, textwrap
from django_anger.migration_utils import forwards_contents
from django_anger.migration_utils import parse_migration

def get_south_apps(project_dir):
    """
    Return a list of South-enabled apps in the given project_dir.

    Assumes an app is South-enabled if it has a 'migrations' directory.
    """
    apps = []
    for app in os.listdir(project_dir):
        dirname = os.path.join(project_dir, app)
        if not os.path.isdir(dirname):
            continue
        if os.path.exists(os.path.join(dirname, 'migrations')):
            apps.append(app)

    return apps


def get_migration_filenames(app_dir):
    """
    Return list of filenames of all migrations in the given app dir.
    """
    filenames = []
    migrations_dir = os.path.join(app_dir, 'migrations')
    for filename in os.listdir(migrations_dir):
        if not filename.endswith('.py'):
            continue
        if filename == '__init__.py':
            continue
        filenames.append(filename)

    return filenames


def get_path_of_sole_initial_migration(app_dir):
    """
    Return path to the sole 0001_initial migration in the given app dir.

    Raise ValueError if the app has other migrations.
    """
    filenames = get_migration_filenames(app_dir)
    if len(filenames) != 1 or filenames[0] != '0001_initial.py':
        raise ValueError(("App '{}' has non-initial migrations.").format(app_dir))
    return os.path.join(app_dir, 'migrations', filenames[0])


_imports = '\n# -*- coding: utf-8 -*-\nimport datetime\nfrom south.db import db\nfrom south.v2 import SchemaMigration\nfrom django.db import models\n'
_class_def = '\nclass Migration(SchemaMigration):\n'
_depends_on = "\n    depends_on = (\n        ('{}', '{}'),\n    )\n"
_forwards = '\n    def forwards(self, orm):\n'
_backwards = '\n    def backwards(self, orm):\n        raise RuntimeError("Cannot reverse this migration.")\n'

def _pretty_print_models(models, output):
    """
    Custom pretty printer for models = { ... } part of a migration.
    """
    print >> output, '\n    models = {'
    for model_name, model_def in sorted(models.items()):
        print >> output, ("        '{}': {{").format(model_name)
        for field_name, field_def in sorted(model_def.items()):
            print >> output, ("            '{}': {},").format(field_name, field_def)

        print >> output, '        },'

    print >> output, '    }'


def _pretty_print_complete_apps(apps, output):
    """
    Custom pretty printer for complete_apps = [ ... ] part of a migration.
    """
    print >> output, '\n    complete_apps = ['
    for app in sorted(apps):
        print >> output, ("        '{}',").format(app)

    print >> output, '    ]'


def squash_migrations(app_to_migration_path):
    """
    Squash many initial migrations into a single migration.

    `app_to_migration_path` is a dict from app name to the path of the initial
    migration for that app.

    Returns the squashed migration as a StringIO object.

    The squashed migration has:
    - no dependencies
    - a forwards() function obtained by concatenating the forwards() functions
      of all the given migrations
    - a backwards() function that raises RuntimeError
    - all frozen models in all the given migrations
    - all complete_apps in all the given migrations
    """
    output = StringIO()
    print >> output, _imports
    print >> output, _class_def
    print >> output, _forwards
    for app, migration_path in sorted(app_to_migration_path.items()):
        print >> output, ('\n        ### {} app ###\n').format(app)
        output.write(forwards_contents(open(migration_path)))

    print >> output, _backwards
    all_models = {}
    for app, migration_path in app_to_migration_path.iteritems():
        models, complete_apps = parse_migration(open(migration_path))
        if complete_apps != [app]:
            raise ValueError(("App '{}' has unexpected complete_apps {}.").format(app, complete_apps))
        all_models.update(models)

    _pretty_print_models(all_models, output)
    _pretty_print_complete_apps(app_to_migration_path.keys(), output)
    return output


def make_dummy_migration(app, migration_path, destination_app, squashed_migration_name):
    """
    Make a new initial migration for an app whose initial migration has been
    squashed.

    `app` is the name of the app for which to create an initial migration.
    `migration_path` is the path to the initial migration for that app.
    `destination_app` is the app containing the new squashed migration.
    `squashed_migration_name` is the name of the squashed migration (without
    the '.py' suffix)

    Returns the new initial migration as a StringIO object.

    The new migration has:
    - a dependency on the squashed migration
    - a forwards() function that does nothing
    - a backwards() function that raises RuntimeError
    - all frozen models in the original migration
    - the complete_apps in the original migration
    """
    output = StringIO()
    print >> output, _imports
    print >> output, _class_def
    print >> output, _depends_on.format(destination_app, squashed_migration_name)
    print >> output, _forwards
    print >> output, '        pass'
    print >> output, _backwards
    models, complete_apps = parse_migration(open(migration_path))
    _pretty_print_models(models, output)
    _pretty_print_complete_apps(complete_apps, output)
    return output


def main():
    import sys
    if len(sys.argv) < 2:
        print __doc__
        sys.exit(1)
    project_dir = os.getcwd()
    apps = get_south_apps(project_dir)
    print 'Found the following apps:'
    for app in sorted(apps):
        print '    ', app

    print
    app_to_migration_path = {}
    for app in apps:
        app_dir = os.path.join(project_dir, app)
        app_to_migration_path[app] = get_path_of_sole_initial_migration(app_dir)

    destination_app = sys.argv[1]
    if destination_app not in apps:
        raise ValueError(("Could not find app '{}' in current directory.").format(destination_app))
    print 'Squashing migrations...'
    squashed_migration_name = '0001_everything'
    squashed_migration_path = os.path.join(destination_app, 'migrations', squashed_migration_name + '.py')
    squashed_migration = squash_migrations(app_to_migration_path)
    with open(squashed_migration_path, 'w') as (f):
        f.write(squashed_migration.getvalue())
    print 'Updating initial migrations...'
    for app in apps:
        migration_path = app_to_migration_path[app]
        if app == destination_app:
            new_path = migration_path.replace('0001', '0002')
            shutil.move(migration_path, new_path)
            migration_path = new_path
        dummy_migration = make_dummy_migration(app, migration_path, destination_app, squashed_migration_name)
        with open(migration_path, 'w') as (f):
            f.write(dummy_migration.getvalue())

    print 'Done.'
    print ("The squashed migration is '{}'.").format(squashed_migration_path)
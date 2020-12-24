# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/management/commands/schemamigration.py
# Compiled at: 2018-07-11 18:15:31
"""
Startmigration command, version 2.
"""
from __future__ import print_function
import sys, os, re, string, random, inspect
from optparse import make_option
try:
    set
except NameError:
    from sets import Set as set

from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.conf import settings
from south.migration import Migrations, migrate_app
from south.models import MigrationHistory
from south.exceptions import NoMigrations
from south.creator import changes, actions, freezer
from south.management.commands.datamigration import Command as DataCommand

class Command(DataCommand):
    option_list = DataCommand.option_list + (
     make_option('--add-model', action='append', dest='added_model_list', type='string', help='Generate a Create Table migration for the specified model.  Add multiple models to this migration with subsequent --add-model parameters.'),
     make_option('--add-field', action='append', dest='added_field_list', type='string', help='Generate an Add Column migration for the specified modelname.fieldname - you can use this multiple times to add more than one column.'),
     make_option('--add-index', action='append', dest='added_index_list', type='string', help='Generate an Add Index migration for the specified modelname.fieldname - you can use this multiple times to add more than one column.'),
     make_option('--initial', action='store_true', dest='initial', default=False, help='Generate the initial schema for the app.'),
     make_option('--auto', action='store_true', dest='auto', default=False, help='Attempt to automatically detect differences from the last migration.'),
     make_option('--empty', action='store_true', dest='empty', default=False, help='Make a blank migration.'),
     make_option('--update', action='store_true', dest='update', default=False, help='Update the most recent migration instead of creating a new one. Rollback this migration if it is already applied.'))
    help = 'Creates a new template schema migration for the given app'
    usage_str = 'Usage: ./manage.py schemamigration appname migrationname [--empty] [--initial] [--auto] [--add-model ModelName] [--add-field ModelName.field_name] [--stdout]'

    def handle(self, app=None, name='', added_model_list=None, added_field_list=None, freeze_list=None, initial=False, auto=False, stdout=False, added_index_list=None, verbosity=1, empty=False, update=False, **options):
        added_model_list = added_model_list or []
        added_field_list = added_field_list or []
        added_index_list = added_index_list or []
        freeze_list = freeze_list or []
        if stdout:
            name = '-'
        if re.search('[^_\\w]', name) and name != '-':
            self.error('Migration names should contain only alphanumeric characters and underscores.')
        if initial and (added_model_list or added_field_list or auto):
            self.error('You cannot use --initial and other options together\n' + self.usage_str)
        if auto and (added_model_list or added_field_list or initial):
            self.error('You cannot use --auto and other options together\n' + self.usage_str)
        if not app:
            self.error('You must provide an app to create a migration for.\n' + self.usage_str)
        app = app.split('.')[(-1)]
        try:
            app_module = models.get_app(app)
        except ImproperlyConfigured:
            print("There is no enabled application matching '%s'." % app)
            return

        migrations = Migrations(app, force_creation=True, verbose_creation=int(verbosity) > 0)
        if auto:
            try:
                last_migration = migrations[(-2 if update else -1)]
            except IndexError:
                self.error('You cannot use --auto on an app with no migrations. Try --initial.')

            if migrations.app_label() not in getattr(last_migration.migration_class(), 'complete_apps', []):
                self.error("You cannot use automatic detection, since the previous migration does not have this whole app frozen.\nEither make migrations using '--freeze %s' or set 'SOUTH_AUTO_FREEZE_APP = True' in your settings.py." % migrations.app_label())
            old_defs = dict((k, v) for k, v in last_migration.migration_class().models.items() if k.split('.')[0] == migrations.app_label())
            new_defs = dict((k, v) for k, v in freezer.freeze_apps([migrations.app_label()]).items() if k.split('.')[0] == migrations.app_label())
            change_source = changes.AutoChanges(migrations=migrations, old_defs=old_defs, old_orm=last_migration.orm(), new_defs=new_defs)
        elif initial:
            change_source = changes.InitialChanges(migrations)
        elif added_model_list or added_field_list or added_index_list:
            change_source = changes.ManualChanges(migrations, added_model_list, added_field_list, added_index_list)
        elif empty:
            change_source = None
        else:
            print('You have not passed any of --initial, --auto, --empty, --add-model, --add-field or --add-index.', file=sys.stderr)
            sys.exit(1)
        if update and not migrations:
            self.error('You cannot use --update on an app with no migrations.')
        if not name:
            if change_source:
                name = change_source.suggest_name()
            if update:
                name = re.sub('^\\d{4}_', '', migrations[(-1)].name())
            if not name:
                self.error('You must provide a name for this migration\n' + self.usage_str)
        forwards_actions = []
        backwards_actions = []
        if change_source:
            for action_name, params in change_source.get_changes():
                try:
                    action_class = getattr(actions, action_name)
                except AttributeError:
                    raise ValueError('Invalid action name from source: %s' % action_name)
                else:
                    action = action_class(**params)
                    action.add_forwards(forwards_actions)
                    action.add_backwards(backwards_actions)
                    print(action.console_line(), file=sys.stderr)

        if auto and not forwards_actions:
            self.error('Nothing seems to have changed.')
        apps_to_freeze = self.calc_frozen_apps(migrations, freeze_list)
        file_contents = self.get_migration_template() % {'forwards': ('\n').join(forwards_actions or ['        pass']), 
           'backwards': ('\n').join(backwards_actions or ['        pass']), 
           'frozen_models': freezer.freeze_apps_to_string(apps_to_freeze), 
           'complete_apps': apps_to_freeze and 'complete_apps = [%s]' % (', ').join(map(repr, apps_to_freeze)) or ''}
        if update:
            last_migration = migrations[(-1)]
            if MigrationHistory.objects.filter(applied__isnull=False, app_name=app, migration=last_migration.name()):
                print('Migration to be updated, %s, is already applied, rolling it back now...' % last_migration.name(), file=sys.stderr)
                migrate_app(migrations, 'current-1', verbosity=verbosity)
            for ext in ('py', 'pyc'):
                old_filename = '%s.%s' % (os.path.join(migrations.migrations_dir(), last_migration.filename), ext)
                if os.path.isfile(old_filename):
                    os.unlink(old_filename)

            migrations.remove(last_migration)
        new_filename = migrations.next_filename(name)
        if name == '-':
            print(file_contents)
        else:
            fp = open(os.path.join(migrations.migrations_dir(), new_filename), 'w')
            fp.write(file_contents)
            fp.close()
            verb = 'Updated' if update else 'Created'
            if empty:
                print('%s %s. You must now edit this migration and add the code for each direction.' % (verb, new_filename), file=sys.stderr)
            else:
                print('%s %s. You can now apply this migration with: ./manage.py migrate %s' % (verb, new_filename, app), file=sys.stderr)
        return

    def get_migration_template(self):
        return MIGRATION_TEMPLATE


MIGRATION_TEMPLATE = '# -*- coding: utf-8 -*-\nfrom south.utils import datetime_utils as datetime\nfrom south.db import db\nfrom south.v2 import SchemaMigration\nfrom django.db import models\n\n\nclass Migration(SchemaMigration):\n\n    def forwards(self, orm):\n%(forwards)s\n\n    def backwards(self, orm):\n%(backwards)s\n\n    models = %(frozen_models)s\n\n    %(complete_apps)s'
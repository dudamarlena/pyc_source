# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/management/commands/datamigration.py
# Compiled at: 2018-07-11 18:15:31
"""
Data migration creation command
"""
from __future__ import print_function
import sys, os, re
from optparse import make_option
try:
    set
except NameError:
    from sets import Set as set

from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from django.db import models
from django.conf import settings
from south.migration import Migrations
from south.exceptions import NoMigrations
from south.creator import freezer

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
     make_option('--freeze', action='append', dest='freeze_list', type='string', help='Freeze the specified app(s). Provide an app name with each; use the option multiple times for multiple apps'),
     make_option('--stdout', action='store_true', dest='stdout', default=False, help='Print the migration to stdout instead of writing it to a file.'))
    help = 'Creates a new template data migration for the given app'
    usage_str = 'Usage: ./manage.py datamigration appname migrationname [--stdout] [--freeze appname]'

    def handle(self, app=None, name='', freeze_list=None, stdout=False, verbosity=1, **options):
        verbosity = int(verbosity)
        freeze_list = freeze_list or []
        if stdout:
            name = '-'
        if re.search('[^_\\w]', name) and name != '-':
            self.error('Migration names should contain only alphanumeric characters and underscores.')
        if not name:
            self.error('You must provide a name for this migration.\n' + self.usage_str)
        if not app:
            self.error('You must provide an app to create a migration for.\n' + self.usage_str)
        try:
            verbosity = int(verbosity)
        except ValueError:
            self.error('Verbosity must be an number.\n' + self.usage_str)

        migrations = Migrations(app, force_creation=True, verbose_creation=verbosity > 0)
        new_filename = migrations.next_filename(name)
        apps_to_freeze = self.calc_frozen_apps(migrations, freeze_list)
        file_contents = self.get_migration_template() % {'frozen_models': freezer.freeze_apps_to_string(apps_to_freeze), 
           'complete_apps': apps_to_freeze and 'complete_apps = [%s]' % (', ').join(map(repr, apps_to_freeze)) or ''}
        if name == '-':
            print(file_contents)
        else:
            fp = open(os.path.join(migrations.migrations_dir(), new_filename), 'w')
            fp.write(file_contents)
            fp.close()
            print('Created %s.' % new_filename, file=sys.stderr)

    def calc_frozen_apps(self, migrations, freeze_list):
        """
        Works out, from the current app, settings, and the command line options,
        which apps should be frozen.
        """
        apps_to_freeze = []
        for to_freeze in freeze_list:
            if '.' in to_freeze:
                self.error("You cannot freeze %r; you must provide an app label, like 'auth' or 'books'." % to_freeze)
            if not models.get_app(to_freeze):
                self.error("You cannot freeze %r; it's not an installed app." % to_freeze)
            apps_to_freeze.append(to_freeze)

        if getattr(settings, 'SOUTH_AUTO_FREEZE_APP', True):
            apps_to_freeze.append(migrations.app_label())
        return apps_to_freeze

    def error(self, message, code=1):
        """
        Prints the error, and exits with the given code.
        """
        print(message, file=sys.stderr)
        sys.exit(code)

    def get_migration_template(self):
        return MIGRATION_TEMPLATE


MIGRATION_TEMPLATE = '# -*- coding: utf-8 -*-\nfrom south.utils import datetime_utils as datetime\nfrom south.db import db\nfrom south.v2 import DataMigration\nfrom django.db import models\n\nclass Migration(DataMigration):\n\n    def forwards(self, orm):\n        "Write your forwards methods here."\n        # Note: Don\'t use "from appname.models import ModelName". \n        # Use orm.ModelName to refer to models in this application,\n        # and orm[\'appname.ModelName\'] for models in other applications.\n\n    def backwards(self, orm):\n        "Write your backwards methods here."\n\n    models = %(frozen_models)s\n\n    %(complete_apps)s\n    symmetrical = True\n'
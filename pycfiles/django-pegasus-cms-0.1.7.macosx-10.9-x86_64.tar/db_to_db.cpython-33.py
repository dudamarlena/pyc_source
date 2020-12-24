# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/pegasus/lib/python3.3/site-packages/pegasus/management/commands/db_to_db.py
# Compiled at: 2015-02-18 15:30:56
# Size of source mod 2**32: 2444 bytes
from optparse import make_option
from django.core import management
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Migrates data between 2 databases'
    option_list = BaseCommand.option_list + (
     make_option('--origin', action='store', dest='origin', default='sqlite', help='Database alias to use as the source of data'),
     make_option('--destination', action='store', dest='destination', default='default', help='Database alias to use as the destination of data'),
     make_option('--dump-file', action='store', dest='dumpfile', default='/tmp/dump.json', help='Name of fixture file'),
     make_option('-e', '--exclude', dest='exclude', action='append', default=[
      'contenttypes', 'sessions.Session', 'south.Migrationhistory', 'auth.Permission'], help="An appname or appname.ModelName to exclude (use multiple --exclude to exclude multiple apps/models). Defaults to ['contenttypes', 'sessions.Session', 'south.Migrationhistory', 'auth.Permission']"))

    def handle(self, *args, **options):
        self.origin = options.get('origin')
        self.destination = options.get('destination')
        self.dumpfile = options.get('dumpfile')
        self.exclude = options.get('exclude')
        self.stdout.write('Setting up destination: %s\n' % self.destination)
        management.call_command('syncdb', database=self.destination, interactive=False, load_initial_data=False)
        management.call_command('migrate', database=self.destination, load_inital_data=False)
        self.stdout.write('Dumping data from origin: %s\n' % self.origin)
        with open(self.dumpfile, 'w+') as (f):
            management.call_command('dumpdata', database=self.origin, use_base_manager=True, use_natrual_keys=True, exclude=self.exclude, stdout=f)
        self.stdout.write('Loading data into destination: %s\n' % self.destination)
        management.call_command('loaddata', self.dumpfile, using=self.destination)
        self.stdout.write('Successfully migrated')
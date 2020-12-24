# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/incoan/codenerix/management/commands/touch.py
# Compiled at: 2017-12-18 07:03:26
# Size of source mod 2**32: 4972 bytes
import os
try:
    from subprocess import getstatusoutput
    pythoncmd = 'python3'
except:
    from commands import getstatusoutput
    pythoncmd = 'python2'

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from codenerix.lib.debugger import Debugger

class Command(BaseCommand, Debugger):
    help = 'Do a touch to the project'

    def add_arguments(self, parser):
        parser.add_argument('-f', action='store_true', dest='f', default=False, help='Keep the command working forever')
        parser.add_argument('--follow', action='store_true', dest='follow', default=False, help='Keep the command working forever')

    def handle(self, *args, **options):
        self.set_name('CODENERIX')
        self.set_debug()
        appname = settings.ROOT_URLCONF.split('.')[0]
        basedir = settings.BASE_DIR
        appdir = os.path.abspath('{}/{}'.format(basedir, appname))
        keepworking = True
        while keepworking:
            self.debug('Collecting...', color='blue')
            status, output = getstatusoutput('{}/manage collectstatic --noinput'.format(appdir))
            if status:
                raise CommandError(output)
            for line in output.split('\n'):
                if line[0:7] == 'Copying':
                    path = line.split("'")[1].replace(appdir, '.')
                    self.debug('    > {}'.format(path))
                elif 'static file copied to' in line or 'static files copied to' in line:
                    done = line.split(' ')[0]
                    linesp = line.split(',')
                    if len(linesp) == 1:
                        total = linesp[0].split(' ')[0]
                    else:
                        total = linesp[1].split(' ')[1]
                    self.debug('{}/{} files copied'.format(done, total), color='cyan')
                else:
                    if 'was already registered. Reloading models is not advised as it can lead to inconsistencies, most notably with related models.' in line:
                        pass
                    else:
                        if 'new_class._meta.apps.register_model(new_class._meta.app_label, new_class)' in line:
                            pass
                        else:
                            if line == '':
                                pass
                            else:
                                self.warning('Unknown string: #{}#'.format(line))

            self.debug('Cleaning...', color='blue')
            status, output = getstatusoutput('{}/manage clean'.format(appdir))
            if status:
                raise CommandError(output)
            self.debug('Touch...', color='blue', tail=False)
            filenames = os.listdir(appdir)
            filenames.sort()
            for name in filenames:
                if name[0:4] == 'wsgi' or name[-4:] == 'wsgi':
                    status, output = getstatusoutput('/usr/bin/touch {}/{}'.format(appdir, name))
                    if status:
                        raise CommandError(output)
                    self.debug(' [{}]'.format(name), color='cyan', header=False, tail=False)

            self.debug(' Done', color='green', header=False)
            if options['follow'] or options['f']:
                self.debug('Hit a ENTER when ready to go or Q to exit (ENTER|q) ', tail=False, color='purple')
                try:
                    key = raw_input().lower()
                except NameError:
                    key = input().lower()
                except KeyboardInterrupt:
                    self.debug(' ', header=False)
                    key = 'q'

                self.debug('', header=False)
                self.debug(' ')
                if key == 'q':
                    self.debug('Quitting!', color='yellow')
                    keepworking = False
            else:
                self.debug('Quitting!', color='yellow')
                keepworking = False
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/br0th3r/salmonete/becas.com/codenerix/management/commands/locales.py
# Compiled at: 2020-01-10 01:23:46
# Size of source mod 2**32: 9152 bytes
import os
try:
    from subprocess import getstatusoutput
    pythoncmd = 'python3'
except:
    from commands import getstatusoutput
    pythoncmd = 'python'

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from codenerix.lib.debugger import Debugger

class Command(BaseCommand, Debugger):
    help = 'Used to build all locales details'

    def add_arguments(self, parser):
        parser.add_argument('--mode', dest='mode', default='suexec', help="Mode used in the environment 'suexec', 'apache' or 'wwwdata'")
        parser.add_argument('--noauto', action='store_true', dest='noauto', default=False, help='Tells the command not to find automatic solution for problems')
        parser.add_argument('--noguess', action='store_true', dest='noguess', default=False, help='Disable guessing user environment')
        parser.add_argument('--clean', action='store_true', dest='clean', default=False, help='Do a full clean by deleting everything before building translations')
        parser.add_argument('--compile', action='store_true', dest='compile', default=False, help='Compile .po files')

    def handle(self, *args, **options):
        mode = options['mode']
        if mode not in ('wwwdata', 'apache', 'suexec'):
            self.print_help('', '')
            raise CommandError("Allowed modes are suexec, apache or wwwdata ('apache' and 'wwwdata' option will force permissions to apache or www-data user, suexec won't touch permissions)")
        self.set_name('CODENERIX')
        self.set_debug()
        appname = settings.ROOT_URLCONF.split('.')[0]
        basedir = settings.BASE_DIR
        appdir = os.path.abspath('{}/{}'.format(basedir, appname))
        noauto = options['noauto']
        if not options['noguess']:
            cmd = "find {} -name 'locale' -exec ls -lR {{}} \\; | grep www-data".format(appdir)
            status, output = getstatusoutput(cmd)
            if status:
                guess = 'suexec'
            else:
                guess = 'wwwdata'
            if guess != mode:
                self.print_help('', '')
                raise CommandError("You have selected mode '{}' but I believe you are using '{}', if sure use --noguess".format(mode, guess))
        self.debug('Creating locales for {}'.format(appname), color='blue')
        if noauto:
            self.debug('Autoconfig mode is OFF', color='yellow')
        apps = []
        length = len(appname)
        for app in settings.INSTALLED_APPS:
            if app[0:length] == appname:
                apps.append(app[length + 1:])

        ERROR = False
        for app in [''] + apps:
            testpath = os.path.abspath('{}/{}/locale'.format(appdir, app).replace('//', '/'))
            if not os.path.exists(testpath):
                if noauto:
                    ERROR = True
                    self.debug("'locale' folder missing at {}/".format(testpath), color='yellow')
                else:
                    self.debug("'locale' folder missing, creating {}/".format(testpath), color='purple')
                    os.mkdir(testpath)

        if ERROR:
            raise CommandError('Some error has happened, can not keep going! (avoid using --noauto to let CODENERIX find a solution)')
        sudo = ''
        if mode == 'apache' or mode == 'wwwdata':
            status, output = getstatusoutput('whoami')
            if status:
                pass
            self.error("Error while executing 'whoami' command")
            raise CommandError(output)
        else:
            if output == 'www-data':
                self.debug("Detected we are 'www-data' user", color='purple')
            else:
                status, output = getstatusoutput('sudo whoami')
        if status:
            self.error("Error while executing 'sudo whoami' command")
            raise CommandError(output)
        else:
            if output == 'root':
                self.debug("Detected we can become 'root' user", color='purple')
                sudo = 'sudo '
            else:
                raise CommandError("You requested 'apache' or 'wwwdata' execution mode but you are not www-data and we can not become root")
            if options['clean']:
                key = ''
                while key not in ('n', 'y'):
                    self.debug("All 'locale' folders are going to be removed, are you sure? (y|n) ", tail=False, color='red')
                    try:
                        key = raw_input().lower()
                    except NameError:
                        key = input().lower()

                    self.debug('', header=False)

                if key == 'y':
                    self.debug('Removing locale folders...', color='red')
                    for app in [''] + apps:
                        testpath = os.path.abspath('{}/{}/locale'.format(appdir, app).replace('//', '/'))
                        if os.path.exists(testpath):
                            self.debug('    > Removing {}'.format(testpath), color='red')
                            cmd = '{}rm -R {}/*'.format(sudo, testpath)
                            status, output = getstatusoutput(cmd)
                            if status:
                                raise CommandError(output)

            else:
                raise CommandError("You requested to clean all 'locale' folders but you answered NO to the previous question, can not keep going!")
            if not options['compile']:
                for code, name in settings.LANGUAGES:
                    self.debug('Processing translations for {}...'.format(name), color='cyan')
                    cmd = '{}{}/manage.py makemessages -v0 --symlinks --ignore env -l {}'.format(sudo, basedir, code)
                    status, output = getstatusoutput(cmd)
                    if status:
                        raise CommandError(output)
                    cmd = '{}{}/manage.py makemessages -v0 --symlinks --ignore env -d djangojs -l {}'.format(sudo, basedir, code)
                    status, output = getstatusoutput(cmd)
                    if status:
                        raise CommandError(output)

            if sudo:
                self.debug('Setting permissions...', color='cyan')
                if mode == 'apache':
                    user = 'apache'
                else:
                    if mode == 'wwwdata':
                        user = 'www-data'
                    else:
                        raise CommandError("Wrong mode for sudo '{}'".format(mode))
                for app in [''] + apps:
                    testpath = os.path.abspath('{}/{}/locale'.format(appdir, app).replace('//', '/'))
                    cmd = 'sudo chown {}.{} {}/ -R'.format(user, user, testpath)
                    status, output = getstatusoutput(cmd)
                    if status:
                        raise CommandError(output)
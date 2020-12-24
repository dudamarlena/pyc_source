# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/django-chuck/django_chuck/commands/create_virtualenv.py
# Compiled at: 2012-06-12 07:31:09
import subprocess
from django_chuck.commands.base import BaseCommand
import os, shutil

class Command(BaseCommand):
    help = 'Create virtualenv'

    def __init__(self):
        super(Command, self).__init__()

    def handle(self, args, cfg):
        super(Command, self).handle(args, cfg)
        if os.path.exists(self.virtualenv_dir):
            answer = raw_input('Delete old virtualenv dir? <y/N>: ')
            if not answer.lower() == 'y' and not answer.lower() == 'j':
                print 'Aborting.'
                return 0
            shutil.rmtree(self.virtualenv_dir)
            os.makedirs(self.virtualenv_dir)
        else:
            os.makedirs(self.virtualenv_dir)
        self.print_header('CREATE VIRTUALENV')
        if self.use_virtualenvwrapper:
            self.execute('. virtualenvwrapper.sh; mkvirtualenv --no-site-packages ' + self.site_name)
            export_dest = open(os.path.join(self.virtualenv_dir, 'bin', 'postactivate'), 'a')
        else:
            self.execute('virtualenv --no-site-packages ' + self.virtualenv_dir)
            export_dest = open(os.path.join(self.virtualenv_dir, 'bin', 'activate'), 'a')
        self.print_header('SETUP VIRTUALENV')
        print 'Destination: %s' % export_dest.name
        print 'Project path: %s' % 'export PYTHONPATH="' + self.site_dir + '":$PYTHONPATH'
        export_dest.write('export PYTHONPATH="' + self.site_dir + '":$PYTHONPATH\n')
        if self.django_settings:
            print 'Project settings: %s' % 'export DJANGO_SETTINGS_MODULE=' + self.django_settings + '\n'
            export_dest.write('export DJANGO_SETTINGS_MODULE=' + self.django_settings + '\n')
        export_dest.close()
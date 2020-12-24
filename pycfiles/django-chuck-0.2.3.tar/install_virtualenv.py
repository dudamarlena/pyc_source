# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/django-chuck/django_chuck/commands/install_virtualenv.py
# Compiled at: 2012-06-13 09:16:40
from django_chuck.commands.base import BaseCommand
import re, os

class Command(BaseCommand):
    help = 'Install all requirements in virtualenv'

    def __init__(self):
        super(Command, self).__init__()
        self.opts.append(('-a',
         {'help': 'Comma seperated list of apps that should get installed by pip', 
            'dest': 'additional_apps', 
            'default': None, 
            'nargs': '?'}))
        return

    def handle(self, args, cfg):
        super(Command, self).handle(args, cfg)
        self.print_header('INSTALL VIRTUALENV')
        self.execute_in_project('pip install -r ' + os.path.join(self.site_dir, 'requirements', 'requirements_local.txt'))
        if self.additional_apps:
            for app in re.split('\\s*,\\s*', self.additional_apps):
                self.execute_in_project('pip install ' + app)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/django-chuck/django_chuck/commands/list_modules.py
# Compiled at: 2012-06-05 03:14:27
import os
from django_chuck.commands.base import BaseCommand

class Command(BaseCommand):
    help = 'Shows all available modules'

    def __init__(self):
        super(Command, self).__init__()
        self.no_default_checks = True

    def handle(self, args, cfg):
        super(Command, self).handle(args, cfg)
        self.print_header('AVAILABLE MODULES')
        for module_basedir in self.module_basedirs:
            for module_name in os.listdir(module_basedir):
                print module_name
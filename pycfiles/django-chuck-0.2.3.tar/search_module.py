# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/django-chuck/django_chuck/commands/search_module.py
# Compiled at: 2012-06-13 09:38:56
import os, re
from django_chuck.commands.base import BaseCommand

class Command(BaseCommand):
    help = 'Search available modules matching given name or description'

    def __init__(self):
        super(Command, self).__init__()
        self.no_default_checks = True
        self.opts = [
         (
          'pattern',
          {'help': 'search pattern', 
             'default': ''})]

    def handle(self, args, cfg):
        super(Command, self).handle(args, cfg)
        self.print_header('MATCHING MODULES')
        for module_name, module in self.get_module_cache().items():
            if re.search(self.args.pattern, module_name) or re.search(self.args.pattern, module.get_description()):
                print '-------------------------------------------------------------------------------'
                print '[%s]' % (module_name,)
                print '-------------------------------------------------------------------------------'
                if module.get_description():
                    print module.get_description() + '\n'
                else:
                    print '\nNo description available\n\n'
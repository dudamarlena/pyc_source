# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/django-chuck/django_chuck/commands/show_info.py
# Compiled at: 2012-06-05 03:14:27
import os
from django_chuck.commands.base import BaseCommand
import imp

class Command(BaseCommand):
    help = 'Shows all available information of a module'

    def __init__(self):
        super(Command, self).__init__()
        self.no_default_checks = True
        self.opts = (
         (
          'module',
          {'help': 'A module name', 
             'default': None, 
             'nargs': '?'}),)
        return

    def show_info(self, module, module_dir):
        self.print_header("Module '%s'" % module)
        print 'Location: \t%s' % module_dir
        chuck_module_file = os.path.join(module_dir, 'chuck_module.py')
        if os.access(chuck_module_file, os.R_OK):
            chuck_module = imp.load_source(module.replace('-', '_'), chuck_module_file)
            if hasattr(chuck_module, 'depends'):
                print 'Dependencies: \t %s' % (', ').join(chuck_module.depends)
            if hasattr(chuck_module, 'description'):
                print chuck_module.description

    def handle(self, args, cfg):
        super(Command, self).handle(args, cfg)
        module = self.arg_or_cfg('module')
        if not module:
            print 'Please provide a module name!'
            return
        else:
            module_dir = None
            for module_basedir in self.module_basedirs:
                if module in os.listdir(module_basedir):
                    module_dir = os.path.join(module_basedir, module)
                    break

            if not module_dir:
                print "No module with name '%s' found!" % module
                return
            self.show_info(module, module_dir)
            return
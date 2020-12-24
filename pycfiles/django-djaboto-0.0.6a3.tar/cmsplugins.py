# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/growlf/django/django-djaboto/djaboto/management/commands/cmsplugins.py
# Compiled at: 2013-02-21 16:38:08
import optparse, pip, xmlrpclib, sys, os
from django.core.management.base import BaseCommand
import djaboto
from subprocess import check_call
from cms.plugin_pool import plugin_pool

class Command(BaseCommand):
    help = 'List all plugins available to this project (not just the ones in use).'
    requires_model_validation = False
    can_import_settings = True

    def handle(self, *args, **options):
        """
        Shows all plugins that are available to this project, not just the ones that are already in use.
        """
        plugin_pool.discover_plugins()
        if options.get('verbosity', 0):
            print '%-45s %s %s MODEL' % ('PLUGIN', 'TEXT ', 'ADMIN')
        for plugin in sorted(plugin_pool.plugins.iterkeys()):
            if options.get('verbosity', 0):
                if plugin_pool.plugins[plugin].module:
                    plugin_str = '%s (%s)' % (plugin, plugin_pool.plugins[plugin].module)
                else:
                    plugin_str = plugin
                print '%-45s %-5s %-5s %s' % (
                 plugin_str,
                 plugin_pool.plugins[plugin].text_enabled,
                 plugin_pool.plugins[plugin].admin_preview,
                 plugin_pool.plugins[plugin].model)
            else:
                print plugin
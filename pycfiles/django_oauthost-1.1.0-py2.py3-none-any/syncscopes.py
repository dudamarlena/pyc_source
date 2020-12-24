# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/idle/projects/gitdev/oauthost/sandbox/oauthost/management/commands/syncscopes.py
# Compiled at: 2011-11-09 10:41:10
from os import path
from inspect import getfile
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import IntegrityError
from oauthost.models import Scope

class Command(BaseCommand):
    args = '<app_name app_name ...>'
    help = 'Registers OAuth2 scopes from application views in form of `<application_name>:<decorated_view_name>`.\nUse @oauth_required to decorate view which requires scope syncing.'

    def handle(self, *args, **options):
        if not len(args):
            raise CommandError('This command accepts space delimited list of application names.')
        if not set(args).issubset(settings.INSTALLED_APPS):
            raise CommandError('One or more application names issued to the command are not in INSTALLED_APPS.')
        for app_name in args:
            decorated_views_count = 0
            self.stdout.write('Working on "%s" application ...\n' % app_name)
            try:
                app_views = __import__('%s.views' % app_name)
            except ImportError:
                raise CommandError('No views.py found in the application.')

            app_views_substr = path.join('oauthost', 'decorators.py')
            for func_name in dir(app_views.views):
                if '__' not in func_name:
                    func = getattr(app_views.views, func_name)
                    if func_name != 'oauth_required' and app_views_substr in getfile(func):
                        decorated_views_count += 1
                        scope_name = '%(app_name)s:%(view_name)s' % {'app_name': app_name, 'view_name': func_name}
                        self.stdout.write('    Found "%s" view. Syncing "%s" scope ... ' % (func_name, scope_name))
                        scope_title = '%s %s' % (app_name.capitalize(), (' ').join([ word.capitalize() for word in func_name.split('_') ]))
                        scope = Scope(identifier=scope_name, title=scope_title)
                        try:
                            scope.save()
                        except IntegrityError:
                            self.stdout.write('WARNING: Scope skipped as already exists\n')
                        else:
                            self.stdout.write('Done\n')

            if not decorated_views_count:
                self.stdout.write('NOTE: No views decorated with "@oauth_required" are found in the application.\n')
            self.stdout.write('\n')
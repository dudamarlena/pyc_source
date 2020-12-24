# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hansek/projects/django_groups_sync/groups_sync/management/commands/sync_groups_permissions.py
# Compiled at: 2020-03-30 03:29:49
# Size of source mod 2**32: 7330 bytes
import json
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Sync User Groups permissions by definition in json file'

    def add_arguments(self, parser):
        parser.add_argument('args',
          metavar='group name', nargs='*', help='A Group name which should only be synchronized (use "" if there are spaces in Group name).')
        parser.add_argument('--file',
          dest='file', help='Specifies json data file.')
        parser.add_argument('--noinput',
          '--no-input', action='store_false', dest='interactive', help='Do NOT prompt the user for input of any kind.')
        parser.add_argument('-n',
          '--dry-run', action='store_true', help='Do everything except modify the database.')

    def handle(self, *group_names, interactive, verbosity, dry_run, **options):
        message = []
        if dry_run:
            print('\nYou have activated the --dry-run option so nothing will be modified.\n')
        else:
            try:
                filepath = options.get('file') or settings.GROUP_SYNC_FILENAME
                with open(filepath) as (file):
                    file_data = json.load(file)
            except FileNotFoundError as e:
                raise CommandError('File "{}" not found.'.format(filepath))

            data_groups = file_data['groups'].keys()
            if group_names:
                for gn in group_names:
                    if gn not in data_groups:
                        raise CommandError('Group "{}" not found in file groups.'.format(gn))

            else:
                group_names = data_groups
        groups = Group.objects.prefetch_related('permissions').filter(name__in=group_names).values_list('name', flat=True)
        groups_to_create = set(group_names).difference(groups)
        groups_to_sync = set(group_names) - groups_to_create
        if not dry_run and interactive:
            if verbosity:
                message.append('')
                if groups_to_create:
                    message.append('Groups to be created: {}'.format('; '.join(groups_to_create)))
                if groups_to_sync:
                    message.append('Groups to be synced: {}'.format('; '.join(groups_to_sync)))
                print('\n'.join(message))
                message = ['']
            if input('\nDo you want to sync? [type "yes" to continue] ') != 'yes':
                print()
                raise CommandError('Group sync cancelled.')
        for g_name in group_names:
            permissions = []
            missing_apps_models = {}
            missing_models_permissions = {}
            for app_label, app_models in file_data['groups'][g_name].items():
                content_types = ContentType.objects.filter(model__in=app_models)
                if content_types.count() != len(app_models):
                    missing_models = set(app_models) - set(content_types.values_list('model', flat=True))
                    missing_apps_models[app_label] = missing_models
                for ct in content_types:
                    ct_permissions = ct.permission_set.filter(codename__in=(app_models[ct.model]))
                    perms_codenames = ct_permissions.values_list('codename', flat=True)
                    if len(perms_codenames) != len(app_models[ct.model]):
                        missing_permissions = set(app_models[ct.model]) - set(perms_codenames)
                        missing_models_permissions[ct.model] = missing_permissions
                    else:
                        permissions.extend(ct_permissions)

            if missing_apps_models or missing_models_permissions:
                if missing_apps_models:
                    message.append('ContentType app models are missing:')
                    for app_label, missing_models in missing_apps_models.items():
                        message.append(' - {}: {}'.format(app_label, ', '.join(missing_models)))

                if missing_models_permissions:
                    if message:
                        message.append('\n')
                    message.append('Model permissions are missing:')
                    for model, perms in missing_models_permissions.items():
                        message.append(' - {}: {}'.format(model, ', '.join(perms)))

                print('\n'.join(message))
                raise CommandError('Group sync cannot continue')
            if dry_run:
                if g_name in groups_to_create:
                    g = Group(name=g_name)
                    group_created = True
                else:
                    g = Group.objects.get(name=g_name)
                    group_created = False
            else:
                g, group_created = Group.objects.get_or_create(name=g_name)
            if group_created:
                to_create = permissions
            else:
                to_create = set(permissions).difference(g.permissions.all())
            if not dry_run:
                (g.permissions.add)(*to_create)
            to_remove = []
            if not group_created:
                to_remove = set(g.permissions.all()) - set(permissions)
                if not dry_run:
                    if to_remove:
                        (g.permissions.remove)(*to_remove)
                    if verbosity and (to_create or to_remove):
                        group_state = 'synced'
                        if group_created:
                            group_state = 'created'
                        elif dry_run and group_created:
                            permissions_count = len(permissions)
                        else:
                            permissions_count = g.permissions.count()
                        message.append('Group "{}" {} and has {} permissions:'.format(g.name, group_state, permissions_count))
                        message.append(' - assigned: {} permissions'.format(len(to_create)))
                        if not group_created:
                            message.append(' - removed: {} permissions'.format(len(to_remove)))
                elif verbosity:
                    message.append('Group "{}" already in sync and has {} permissions.'.format(g.name, g.permissions.count()))

        if verbosity:
            message.append('\nDone...')
            print('\n'.join(message))
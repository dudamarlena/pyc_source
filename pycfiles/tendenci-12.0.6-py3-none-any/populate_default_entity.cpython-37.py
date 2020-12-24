# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/entities/management/commands/populate_default_entity.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 5351 bytes
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import django.apps as apps

class Command(BaseCommand):
    __doc__ = '\n    Loop through all models that are subclasses of the TendenciBaseModel\n    and populate the entity with the default entity (id=1). If no entity\n    exists, create one first.\n\n    Also, check if we have a group with the same name of site\n    display name and associated to the default entity (id=1).\n    If not found, create one.\n\n    Usage:\n        python manage.py populate_default_entity --verbosity=2\n    '

    def handle(self, *args, **options):
        from tendenci.apps.entities.models import Entity
        from tendenci.apps.user_groups.models import Group
        from tendenci.apps.site_settings.utils import get_setting
        from tendenci.apps.perms.models import TendenciBaseModel
        verbosity = int(options['verbosity'])
        entity, = Entity.objects.filter(pk=1)[:1] or [None]
        user, = User.objects.filter(pk=1)[:1] or [None]
        site_display_name = get_setting('site', 'global', 'sitedisplayname')
        if not site_display_name:
            site_display_name = 'Default'
        else:
            site_contact_name = get_setting('site', 'global', 'sitecontactname')
            site_contact_email = get_setting('site', 'global', 'sitecontactemail')
            site_phone_number = get_setting('site', 'global', 'sitephonenumber')
            site_url = get_setting('site', 'global', 'siteurl')
            if not entity:
                params = {'id':1, 
                 'entity_name':site_display_name, 
                 'entity_type':'', 
                 'contact_name':site_contact_name, 
                 'phone':site_phone_number, 
                 'email':site_contact_email, 
                 'fax':'', 
                 'website':site_url, 
                 'summary':'', 
                 'notes':'', 
                 'admin_notes':'system auto created', 
                 'allow_anonymous_view':True, 
                 'status':True, 
                 'status_detail':'active'}
                if user:
                    params.update({'creator':user,  'creator_username':user.username, 
                     'owner':user, 
                     'owner_username':user.username})
                else:
                    params.update({'creator_username':'',  'owner_username':''})
                entity = Entity(**params)
                entity.save()
                print('entity created: ', entity.entity_name)
            models = apps.get_models()
            tables_excluded = [
             'corporate_memberships_corporatemembership',
             'corporate_memberships_corporatemembershiparchive']
            table_updated = []
            for model in models:
                if TendenciBaseModel in model.__bases__:
                    if hasattr(model, 'entity'):
                        table_name = model._meta.db_table
                        if table_name in tables_excluded:
                            continue
                    for row in model.objects.all():
                        if not row.entity:
                            row.entity = entity
                            row.save(update_fields=['entity'])

                    table_updated.append(table_name)

            if verbosity >= 2:
                print()
                print('List of tables updated: ')
                print('\n'.join(table_updated))
                print()
            group_exists = Group.objects.filter(entity=entity).exists()
            params = group_exists or {'name':site_display_name, 
             'entity':entity, 
             'type':'distribution', 
             'email_recipient':site_contact_email, 
             'allow_anonymous_view':True, 
             'status':True, 
             'status_detail':'active'}
            if user:
                params.update({'creator':user,  'creator_username':user.username, 
                 'owner':user, 
                 'owner_username':user.username})
            else:
                params.update({'creator_username':'',  'owner_username':''})
        group = Group(**params)
        try:
            group.save()
            print('Group created: ', group.name)
        except Exception as e:
            try:
                print(e)
            finally:
                e = None
                del e

        print('All done.')
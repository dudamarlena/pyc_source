# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/user_groups/management/commands/populate_entity_and_auth_group_columns.py
# Compiled at: 2020-02-26 14:49:28
# Size of source mod 2**32: 947 bytes
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    __doc__ = '"\n    Populate the blank entity and auth group fields for the user groups.\n    For the blank entity field, fill out with the default entity (id=1).\n    For the blank auth group field, get or create one by name if not exists.\n\n    Usage: ./manage.py populate_entity_and_auth_group_columns\n    '

    def handle(self, *args, **options):
        from tendenci.apps.entities.models import Entity
        from tendenci.apps.user_groups.models import Group
        groups = Group.objects.all()
        if groups:
            first_entity = Entity.objects.first()
            for ugroup in groups:
                if not ugroup.entity:
                    ugroup.entity = first_entity
                    ugroup.save()
                if not ugroup.group:
                    ugroup.save()
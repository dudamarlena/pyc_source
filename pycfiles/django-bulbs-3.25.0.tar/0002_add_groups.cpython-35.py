# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/content/migrations/0002_add_groups.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 1649 bytes
from __future__ import unicode_literals
from django.db import models, migrations

def create_default_groups(apps, schema_editors):
    PERM_CONF = {'publish_content': 'Can publish content', 
     'publish_own_content': 'Can publish own content', 
     'change_content': 'Can change content', 
     'promote_content': 'Can promote content'}
    GROUP_CONF = dict(contributor=(), author=('publish_own_content', ), editor=('publish_content',
                                                                                'change_content',
                                                                                'promote_content'), admin=('publish_content',
                                                                                                           'change_content',
                                                                                                           'promote_content'))
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    content_ct, _ = ContentType.objects.get_or_create(model='content', app_label='content')
    for group_name, group_perms in GROUP_CONF.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        for perm_name in group_perms:
            perm, _ = Permission.objects.get_or_create(content_type=content_ct, codename=perm_name, defaults={'name': PERM_CONF[perm_name]})
            group.permissions.add(perm)


class Migration(migrations.Migration):
    dependencies = [
     ('content', '0001_initial')]
    operations = [
     migrations.RunPython(create_default_groups, lambda x, y: None)]
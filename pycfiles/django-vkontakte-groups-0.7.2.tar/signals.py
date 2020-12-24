# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-groups/vkontakte_groups/signals.py
# Compiled at: 2015-11-01 17:29:28
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from m2m_history.models import ManyToManyHistoryVersion

@receiver(post_save, sender=ManyToManyHistoryVersion)
def fetch_new_users_members(sender, instance, created, **kwargs):
    if 'vkontakte_users' in settings.INSTALLED_APPS and instance.field_name == 'members' and created and instance.content_type.app_label == 'vkontakte_groups' and instance.content_type.model == 'group':
        from vkontakte_users.signals import users_to_fetch
        versions = getattr(instance.object, instance.field_name).versions
        new_ids = instance.items(only_pk=True) if versions.count() == 1 else instance.added(only_pk=True)
        new_ids = list(new_ids)
        users_to_fetch.send(sender=sender, ids=new_ids)
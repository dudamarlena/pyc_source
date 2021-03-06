# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/notifications/migrations/0003_auto_20190517_1651.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1328 bytes
from django.db import migrations
from aparnik.contrib.notifications.models import NotificationType

def add_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Notification = apps.get_model('notifications', 'Notification')
    for notification in Notification.objects.all():
        notification.notification_send_type = NotificationType.ALL_USER if notification.is_for_all_users else NotificationType.SINGLE_USER
        notification.save()


def remove_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Notification = apps.get_model('notifications', 'Notification')
    for notification in Notification.objects.all():
        notification.is_for_all_users = notification.notification_send_type == NotificationType.ALL_USER
        notification.save()


class Migration(migrations.Migration):
    dependencies = [
     ('notifications', '0002_notification_notification_send_type')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=remove_keys)]
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0026_auto_20190526_1210.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1215 bytes
from django.db import migrations
from aparnik.contrib.users.models import DeviceType

def add_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    DeviceLogin = apps.get_model('aparnik_users', 'devicelogin')
    for device in DeviceLogin.objects.all():
        device.device_type = DeviceType.ANDROID if device.device_type_temp == 'a' else DeviceType.IOS
        device.save()


def remove_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    DeviceLogin = apps.get_model('aparnik_users', 'devicelogin')
    for device in DeviceLogin.objects.all():
        device.device_type_temp = 'a' if device.device_type == DeviceType.ANDROID else 'i'
        device.save()


class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0025_auto_20190526_1210')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=remove_keys)]
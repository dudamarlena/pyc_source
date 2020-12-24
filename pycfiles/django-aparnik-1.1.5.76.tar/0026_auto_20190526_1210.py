# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0026_auto_20190526_1210.py
# Compiled at: 2019-05-26 05:26:21
from __future__ import unicode_literals
from django.db import migrations
from aparnik.contrib.users.models import DeviceType

def add_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    DeviceLogin = apps.get_model(b'aparnik_users', b'devicelogin')
    for device in DeviceLogin.objects.all():
        device.device_type = DeviceType.ANDROID if device.device_type_temp == b'a' else DeviceType.IOS
        device.save()


def remove_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    DeviceLogin = apps.get_model(b'aparnik_users', b'devicelogin')
    for device in DeviceLogin.objects.all():
        device.device_type_temp = b'a' if device.device_type == DeviceType.ANDROID else b'i'
        device.save()


class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0025_auto_20190526_1210')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=remove_keys)]
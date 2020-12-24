# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0024_devicelogin_device_type.py
# Compiled at: 2019-05-26 05:17:53
from __future__ import unicode_literals
import aparnik.contrib.users.models
from django.db import migrations
import django_enumfield.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0023_auto_20190526_1043')]
    operations = [
     migrations.AddField(model_name=b'devicelogin', name=b'device_type', field=django_enumfield.db.fields.EnumField(default=0, blank=True, enum=aparnik.contrib.users.models.DeviceType, null=True, verbose_name=b'Device Type'))]
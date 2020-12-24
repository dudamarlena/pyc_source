# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0025_auto_20190526_1210.py
# Compiled at: 2019-05-26 03:40:05
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0024_devicelogin_device_type')]
    operations = [
     migrations.AlterField(model_name=b'devicelogin', name=b'device_type_temp', field=models.CharField(blank=True, choices=[('a', 'Android'), ('i', 'iOS')], max_length=1, null=True, verbose_name=b'Device Type'))]
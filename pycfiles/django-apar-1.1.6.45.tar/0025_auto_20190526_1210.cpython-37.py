# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0025_auto_20190526_1210.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 530 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0024_devicelogin_device_type')]
    operations = [
     migrations.AlterField(model_name='devicelogin',
       name='device_type_temp',
       field=models.CharField(blank=True, choices=[('a', 'Android'), ('i', 'iOS')], max_length=1, null=True, verbose_name='Device Type'))]
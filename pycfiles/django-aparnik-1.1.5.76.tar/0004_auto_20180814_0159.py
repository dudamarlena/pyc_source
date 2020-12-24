# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0004_auto_20180814_0159.py
# Compiled at: 2018-10-16 22:51:53
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0003_user_verify_mobile')]
    operations = [
     migrations.AddField(model_name=b'devicelogin', name=b'device_type', field=models.CharField(choices=[('a', 'Android'), ('i', 'iOS')], default=b'a', max_length=1, verbose_name=b'Device Type'), preserve_default=False),
     migrations.AddField(model_name=b'devicelogin', name=b'is_active', field=models.BooleanField(default=True, verbose_name=b'Is Active'))]
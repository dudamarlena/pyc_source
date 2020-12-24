# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0012_auto_20190211_1416.py
# Compiled at: 2019-02-15 10:41:34
from __future__ import unicode_literals
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0011_auto_20181202_1529')]
    operations = [
     migrations.AddField(model_name=b'user', name=b'created_at', field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name=b'Created at'), preserve_default=False),
     migrations.AddField(model_name=b'user', name=b'update_at', field=models.DateTimeField(auto_now=True, verbose_name=b'Update at'))]
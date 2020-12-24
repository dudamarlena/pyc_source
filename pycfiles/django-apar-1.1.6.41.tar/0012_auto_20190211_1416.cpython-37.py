# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0012_auto_20190211_1416.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 735 bytes
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0011_auto_20181202_1529')]
    operations = [
     migrations.AddField(model_name='user',
       name='created_at',
       field=models.DateTimeField(auto_now_add=True, default=(django.utils.timezone.now), verbose_name='Created at'),
       preserve_default=False),
     migrations.AddField(model_name='user',
       name='update_at',
       field=models.DateTimeField(auto_now=True, verbose_name='Update at'))]
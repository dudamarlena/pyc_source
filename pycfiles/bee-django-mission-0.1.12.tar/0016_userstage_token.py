# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_mission/migrations/0016_userstage_token.py
# Compiled at: 2019-01-11 02:54:14
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_mission', '0015_auto_20181219_2057')]
    operations = [
     migrations.AddField(model_name=b'userstage', name=b'token', field=models.CharField(max_length=180, null=True, verbose_name=b'相同一类阶段任务的token'))]
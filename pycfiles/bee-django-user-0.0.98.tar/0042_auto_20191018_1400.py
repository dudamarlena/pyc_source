# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0042_auto_20191018_1400.py
# Compiled at: 2019-10-18 02:00:32
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0041_auto_20191018_1359')]
    operations = [
     migrations.AlterField(model_name=b'userlevel', name=b'req', field=models.TextField(blank=True, null=True, verbose_name=b'申请要求'))]
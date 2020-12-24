# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0029_auto_20190923_1715.py
# Compiled at: 2019-09-23 05:15:17
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0028_auto_20190911_1541')]
    operations = [
     migrations.AlterField(model_name=b'preuser', name=b'gender', field=models.IntegerField(blank=True, choices=[(1, '男'), (2, '女')], default=0, null=True, verbose_name=b'性别'))]
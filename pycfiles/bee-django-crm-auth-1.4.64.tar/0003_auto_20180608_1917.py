# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0003_auto_20180608_1917.py
# Compiled at: 2018-06-14 06:29:04
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0002_auto_20180517_1758')]
    operations = [
     migrations.AlterField(model_name=b'preuser', name=b'mobile', field=models.CharField(max_length=15, verbose_name=b'电话'))]
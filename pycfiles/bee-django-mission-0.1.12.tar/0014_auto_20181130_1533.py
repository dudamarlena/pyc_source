# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_mission/migrations/0014_auto_20181130_1533.py
# Compiled at: 2018-11-30 02:33:37
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_mission', '0013_auto_20181130_1346')]
    operations = [
     migrations.AlterField(model_name=b'missiontype', name=b'conditions', field=models.TextField(blank=True, help_text=b'格式为：[条件1：值1;条件2：值2]，多个条件用;分割', null=True, verbose_name=b'其他附加条件'))]
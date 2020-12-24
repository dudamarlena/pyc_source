# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_mission/migrations/0004_missiontype_line_type.py
# Compiled at: 2018-06-14 06:29:04
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_mission', '0003_auto_20180529_1844')]
    operations = [
     migrations.AddField(model_name=b'missiontype', name=b'line_type', field=models.IntegerField(choices=[(0, '无'), (1, 'url后面接user.id')], default=0, verbose_name=b'对值运算'))]
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_mission/migrations/0003_auto_20180529_1844.py
# Compiled at: 2018-06-14 06:29:04
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_mission', '0002_userstage_stutas')]
    operations = [
     migrations.AlterModelOptions(name=b'line', options={b'ordering': [b'id'], b'permissions': (('can_manage_mission', '可以进入mission管理页'), ), b'verbose_name': b'任务线'}),
     migrations.AlterField(model_name=b'mission', name=b'count', field=models.IntegerField(verbose_name=b'要求数量')),
     migrations.AlterField(model_name=b'mission', name=b'mission_type', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=b'bee_django_mission.MissionType', verbose_name=b'任务类型')),
     migrations.AlterField(model_name=b'mission', name=b'stage', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=b'bee_django_mission.Stage', verbose_name=b'所属阶段'))]
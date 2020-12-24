# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_mission/migrations/0008_customusermission.py
# Compiled at: 2018-06-14 06:29:04
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_mission', '0007_auto_20180613_1555')]
    operations = [
     migrations.CreateModel(name=b'CustomUserMission', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'custom_name', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'自定义名字')),
      (
       b'custom_count', models.IntegerField(blank=True, null=True, verbose_name=b'自定义数量')),
      (
       b'mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_mission.Mission')),
      (
       b'stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_mission.Stage')),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))], options={b'ordering': [
                    b'pk'], 
        b'db_table': b'bee_django_mission_custom_user_mission', 
        b'verbose_name': b'学生自定义任务'})]
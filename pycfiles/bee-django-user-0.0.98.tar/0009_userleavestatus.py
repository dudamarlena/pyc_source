# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0009_userleavestatus.py
# Compiled at: 2018-10-30 01:37:02
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_user', '0008_auto_20181030_1316')]
    operations = [
     migrations.CreateModel(name=b'UserLeaveStatus', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'status', models.IntegerField(default=0)),
      (
       b'leave_start', models.DateTimeField(blank=True, null=True, verbose_name=b'请假开始日期')),
      (
       b'leave_end', models.DateTimeField(blank=True, null=True, verbose_name=b'请假结束日期')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'update_at', models.DateTimeField(auto_now=True)),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))], options={b'ordering': [
                    b'-created_at'], 
        b'db_table': b'bee_django_user_leave_status'})]
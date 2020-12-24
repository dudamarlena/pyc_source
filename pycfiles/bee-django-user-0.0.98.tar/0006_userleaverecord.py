# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0006_userleaverecord.py
# Compiled at: 2018-10-26 05:20:59
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_user', '0005_auto_20181016_1619')]
    operations = [
     migrations.CreateModel(name=b'UserLeaveRecord', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'type', models.IntegerField(choices=[(1, '请假'), (2, '销假'), (3, '延期')], default=1)),
      (
       b'start', models.DateTimeField(blank=True, null=True, verbose_name=b'开始日期')),
      (
       b'end', models.DateTimeField(blank=True, null=True, verbose_name=b'结束日期')),
      (
       b'old_expire', models.DateTimeField(blank=True, verbose_name=b'原结课日期')),
      (
       b'new_expire', models.DateTimeField(blank=True, verbose_name=b'新结课日期')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'is_check', models.BooleanField(default=False, verbose_name=b'通过审核')),
      (
       b'check_at', models.DateTimeField(null=True)),
      (
       b'check_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'leave_user', to=settings.AUTH_USER_MODEL))], options={b'ordering': [
                    b'-created_at'], 
        b'db_table': b'bee_django_user_leave_record', 
        b'permissions': (('change_check', '可以审核用户的请假'), )})]
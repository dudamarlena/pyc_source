# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0018_auto_20190522_1635.py
# Compiled at: 2019-05-22 04:35:20
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0017_userprofile_is_pause')]
    operations = [
     migrations.CreateModel(name=b'UserSN', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'start', models.IntegerField(unique=True, verbose_name=b'起')),
      (
       b'end', models.IntegerField(unique=True, verbose_name=b'起')),
      (
       b'is_used', models.BooleanField(default=False, verbose_name=b'是否正在使用'))]),
     migrations.AlterModelOptions(name=b'userprofile', options={b'ordering': [b'-created_at'], b'permissions': (('can_manage', '可以访问后台管理'), ('can_change_user_group', '可以修改用户组'), ('can_change_user_sn', '可以修改sn号'), ('reset_user_password', '可以重置用户密码'), ('view_all_users', '可以查看所有用户'), ('view_manage_users', '可以查看管理的用户'), ('view_teach_users', '可以查看教的用户'))}),
     migrations.AddField(model_name=b'userprofile', name=b'sn', field=models.IntegerField(null=True, unique=True, verbose_name=b'统一缦客号'))]
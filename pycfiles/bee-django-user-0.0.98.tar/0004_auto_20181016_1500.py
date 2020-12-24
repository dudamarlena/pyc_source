# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0004_auto_20181016_1500.py
# Compiled at: 2018-10-16 03:00:17
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0003_auto_20180517_1641')]
    operations = [
     migrations.AlterModelOptions(name=b'userprofile', options={b'ordering': [b'-created_at'], b'permissions': (('can_manage', '可以访问后台管理'), ('can_change_user_group', '可以修改用户组'), ('reset_user_password', '可以重置用户密码'), ('view_all_users', '可以查看所有用户'), ('view_manage_users', '可以查看管理的用户'), ('view_teach_users', '可以查看教的用户'))})]
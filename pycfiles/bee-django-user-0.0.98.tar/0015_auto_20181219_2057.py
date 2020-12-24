# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0015_auto_20181219_2057.py
# Compiled at: 2018-12-19 07:57:46
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0014_remove_userprofile_is_leave')]
    operations = [
     migrations.AlterModelOptions(name=b'userleaverecord', options={b'ordering': [b'-created_at'], b'permissions': (('update_type_cancel', '可以销假'), ('change_check', '可以审核用户的请假'))})]
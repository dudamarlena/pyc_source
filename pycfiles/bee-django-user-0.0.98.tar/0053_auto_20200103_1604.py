# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0053_auto_20200103_1604.py
# Compiled at: 2020-01-03 03:04:51
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0052_auto_20191213_1503')]
    operations = [
     migrations.AlterModelOptions(name=b'userclassremoverecord', options={b'ordering': [b'-created_at'], b'permissions': (('view_user_class_remove_records', 'view_user_class_remove_records'), )})]
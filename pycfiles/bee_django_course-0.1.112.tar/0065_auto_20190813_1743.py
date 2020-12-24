# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0065_auto_20190813_1743.py
# Compiled at: 2019-08-13 05:43:45
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0064_auto_20190710_1507')]
    operations = [
     migrations.AlterModelOptions(name=b'userlive', options={b'ordering': [b'-created_at'], b'permissions': (('view_all_userlives', '可以查看所有学生的录播'), ('view_teach_userlives', '可以查看所教的学生的录播'), ('view_child_userlives', '可以查看亲子学生的录播'), ('view_expired_userlives', '可以查看超过指定时间的录播')), b'verbose_name': b'course学生录播'})]
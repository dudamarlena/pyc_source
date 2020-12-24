# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0032_auto_20180517_1848.py
# Compiled at: 2018-06-14 06:29:04
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0031_auto_20180516_1714')]
    operations = [
     migrations.AlterModelOptions(name=b'course', options={b'ordering': [b'-id'], b'permissions': (('can_manage_course', '可以进入课程管理页'), ('can_choose_course', 'can choose course')), b'verbose_name': b'course课程'})]
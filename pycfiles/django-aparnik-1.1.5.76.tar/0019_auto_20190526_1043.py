# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/migrations/0019_auto_20190526_1043.py
# Compiled at: 2019-05-26 02:13:35
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('courses', '0018_remove_coursefile_time')]
    operations = [
     migrations.AlterModelOptions(name=b'coursesummary', options={b'ordering': ('id', ), b'verbose_name': b'خلاصه دوره', b'verbose_name_plural': b'خلاصه دوره'})]
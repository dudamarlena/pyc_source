# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/migrations/0010_auto_20181205_1107.py
# Compiled at: 2018-12-05 02:38:14
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('courses', '0009_auto_20181105_1424')]
    operations = [
     migrations.AlterModelOptions(name=b'basecourse', options={b'verbose_name': b'دوره پایه', b'verbose_name_plural': b'دوره های پایه'}),
     migrations.AlterModelOptions(name=b'course', options={b'verbose_name': b'دوره', b'verbose_name_plural': b'دوره ها'})]
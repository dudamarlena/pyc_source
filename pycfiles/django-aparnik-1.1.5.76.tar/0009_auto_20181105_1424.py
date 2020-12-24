# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/migrations/0009_auto_20181105_1424.py
# Compiled at: 2018-11-05 07:19:14
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('courses', '0008_auto_20181105_1424')]
    operations = [
     migrations.AlterField(model_name=b'coursefile', name=b'seconds', field=models.BigIntegerField(default=0, verbose_name=b'زمان')),
     migrations.AlterField(model_name=b'coursesummary', name=b'total_time_seconds', field=models.BigIntegerField(default=0, verbose_name=b'زمان'))]
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/migrations/0008_auto_20181105_1424.py
# Compiled at: 2018-11-05 07:19:14
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('courses', '0007_auto_20181104_1050')]
    operations = [
     migrations.AlterField(model_name=b'coursefile', name=b'seconds', field=models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name=b'زمان')),
     migrations.AlterField(model_name=b'coursesummary', name=b'total_time_seconds', field=models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name=b'زمان'))]
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0024_auto_20180331_1011.py
# Compiled at: 2018-04-01 07:32:39
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0023_auto_20180330_1513')]
    operations = [
     migrations.RemoveField(model_name=b'userassignment', name=b'comment'),
     migrations.RemoveField(model_name=b'userassignment', name=b'rejected_at'),
     migrations.RemoveField(model_name=b'userassignment', name=b'reviewed_at'),
     migrations.RemoveField(model_name=b'userassignment', name=b'status'),
     migrations.RemoveField(model_name=b'userassignment', name=b'submit_at'),
     migrations.RemoveField(model_name=b'userassignment', name=b'updated_at'),
     migrations.RemoveField(model_name=b'userassignment', name=b'work_time'),
     migrations.RemoveField(model_name=b'usercoursesection', name=b'passed_at'),
     migrations.AddField(model_name=b'usercoursesection', name=b'comment', field=models.TextField(blank=True, null=True, verbose_name=b'评语')),
     migrations.AddField(model_name=b'usercoursesection', name=b'updated_at', field=models.DateTimeField(blank=True, null=True)),
     migrations.AddField(model_name=b'usercoursesection', name=b'work_time', field=models.IntegerField(blank=True, default=0, null=True, verbose_name=b'总共练习时间'))]
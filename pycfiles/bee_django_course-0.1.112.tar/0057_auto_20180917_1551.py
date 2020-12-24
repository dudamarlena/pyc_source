# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0057_auto_20180917_1551.py
# Compiled at: 2018-09-17 03:51:18
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0056_coursesectionmid_pionts')]
    operations = [
     migrations.RemoveField(model_name=b'section', name=b'pre_name'),
     migrations.AddField(model_name=b'coursesectionmid', name=b'pre_name', field=models.CharField(blank=True, max_length=180, null=True, verbose_name=b'前缀标题'))]
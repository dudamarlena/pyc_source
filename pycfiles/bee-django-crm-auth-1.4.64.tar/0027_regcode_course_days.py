# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0027_regcode_course_days.py
# Compiled at: 2019-07-15 01:42:52
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0026_auto_20190711_1718')]
    operations = [
     migrations.AddField(model_name=b'regcode', name=b'course_days', field=models.IntegerField(null=True, verbose_name=b'可学习课程天数'))]
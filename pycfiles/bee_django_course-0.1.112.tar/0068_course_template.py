# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0068_course_template.py
# Compiled at: 2019-08-21 01:15:54
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0067_auto_20190819_1414')]
    operations = [
     migrations.AddField(model_name=b'course', name=b'template', field=models.CharField(blank=True, max_length=180, null=True, verbose_name=b'模版'))]
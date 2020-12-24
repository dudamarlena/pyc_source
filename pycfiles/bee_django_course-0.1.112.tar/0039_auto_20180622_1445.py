# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0039_auto_20180622_1445.py
# Compiled at: 2018-06-26 00:36:23
from __future__ import unicode_literals
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0038_auto_20180617_1423')]
    operations = [
     migrations.AlterField(model_name=b'usercoursesection', name=b'updated_at', field=models.DateTimeField(default=django.utils.timezone.now))]
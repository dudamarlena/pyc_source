# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0014_course_is_auto_open.py
# Compiled at: 2019-04-23 03:57:04
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course_simple', '0013_auto_20190421_1848')]
    operations = [
     migrations.AddField(model_name=b'course', name=b'is_auto_open', field=models.BooleanField(default=False, verbose_name=b'是否自动开启'))]
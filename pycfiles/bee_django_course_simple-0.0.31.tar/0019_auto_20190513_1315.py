# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0019_auto_20190513_1315.py
# Compiled at: 2019-05-13 01:15:53
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course_simple', '0018_auto_20190513_1312')]
    operations = [
     migrations.RemoveField(model_name=b'part', name=b'pre_title'),
     migrations.RemoveField(model_name=b'section', name=b'pre_title')]
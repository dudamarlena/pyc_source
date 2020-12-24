# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0008_usersection_started_at.py
# Compiled at: 2019-04-21 03:20:03
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course_simple', '0007_auto_20190418_1409')]
    operations = [
     migrations.AddField(model_name=b'usersection', name=b'started_at', field=models.DateTimeField(blank=True, null=True))]
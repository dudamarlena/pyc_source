# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0028_userquestion_is_correct.py
# Compiled at: 2019-11-06 02:45:41
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course_simple', '0027_auto_20190601_1514')]
    operations = [
     migrations.AddField(model_name=b'userquestion', name=b'is_correct', field=models.BooleanField(default=True))]
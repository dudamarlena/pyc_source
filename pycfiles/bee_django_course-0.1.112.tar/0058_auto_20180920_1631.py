# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0058_auto_20180920_1631.py
# Compiled at: 2018-09-20 04:31:33
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0057_auto_20180917_1551')]
    operations = [
     migrations.RenameField(model_name=b'coursesectionmid', old_name=b'pionts', new_name=b'points')]
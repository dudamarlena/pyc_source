# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0071_userlive_is_mentor_view.py
# Compiled at: 2019-09-06 04:34:22
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0070_userlive_is_star')]
    operations = [
     migrations.AddField(model_name=b'userlive', name=b'is_mentor_view', field=models.BooleanField(default=False))]
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0072_userlive_view_mentor_id.py
# Compiled at: 2019-09-11 03:49:35
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0071_userlive_is_mentor_view')]
    operations = [
     migrations.AddField(model_name=b'userlive', name=b'view_mentor_id', field=models.IntegerField(null=True))]
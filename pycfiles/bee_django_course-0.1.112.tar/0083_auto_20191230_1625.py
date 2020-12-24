# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0083_auto_20191230_1625.py
# Compiled at: 2019-12-30 03:25:20
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0082_userlive_ucs')]
    operations = [
     migrations.RemoveField(model_name=b'userlive', name=b'ucs'),
     migrations.AddField(model_name=b'usercertifyrecord', name=b'user_live', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.UserLive'))]
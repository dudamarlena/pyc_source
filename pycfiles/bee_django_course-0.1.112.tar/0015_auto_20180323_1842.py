# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangwei/code/reusable_app_project/bee_django_course/migrations/0015_auto_20180323_1842.py
# Compiled at: 2018-03-23 06:42:32
from __future__ import unicode_literals
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0014_auto_20180322_1313')]
    operations = [
     migrations.AddField(model_name=b'course', name=b'created_at', field=models.DateTimeField(default=django.utils.timezone.now)),
     migrations.AddField(model_name=b'section', name=b'created_at', field=models.DateTimeField(default=django.utils.timezone.now))]
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangwei/code/reusable_app_project/bee_django_course/migrations/0009_auto_20180318_0016.py
# Compiled at: 2018-03-17 20:16:09
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0008_auto_20180317_0958')]
    operations = [
     migrations.AddField(model_name=b'section', name=b'textwork_info', field=models.TextField(blank=True, null=True, verbose_name=b'作业说明')),
     migrations.AlterField(model_name=b'section', name=b'info', field=models.TextField(blank=True, null=True, verbose_name=b'正文'))]
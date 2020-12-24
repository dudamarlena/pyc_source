# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangwei/code/reusable_app_project/bee_django_course/migrations/0008_auto_20180317_0958.py
# Compiled at: 2018-03-17 05:58:09
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0007_auto_20180317_0917')]
    operations = [
     migrations.AlterField(model_name=b'section', name=b'info', field=models.TextField(blank=True, max_length=180, null=True, verbose_name=b'说明'))]
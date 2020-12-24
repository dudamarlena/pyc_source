# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0031_auto_20180516_1714.py
# Compiled at: 2018-06-14 06:29:04
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0030_preference')]
    operations = [
     migrations.AddField(model_name=b'video', name=b'info', field=models.TextField(blank=True, null=True, verbose_name=b'说明')),
     migrations.AlterField(model_name=b'video', name=b'title', field=models.CharField(max_length=180, null=True, verbose_name=b'标题'))]
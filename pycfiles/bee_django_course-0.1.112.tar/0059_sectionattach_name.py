# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0059_sectionattach_name.py
# Compiled at: 2018-09-28 03:17:41
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0058_auto_20180920_1631')]
    operations = [
     migrations.AddField(model_name=b'sectionattach', name=b'name', field=models.CharField(blank=True, max_length=180, null=True, verbose_name=b'附件名称'))]
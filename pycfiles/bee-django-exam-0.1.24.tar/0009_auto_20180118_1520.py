# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_exam/migrations/0009_auto_20180118_1520.py
# Compiled at: 2018-01-18 02:20:06
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_exam', '0008_auto_20180114_1558')]
    operations = [
     migrations.AlterField(model_name=b'userexamrecord', name=b'passed_date', field=models.CharField(max_length=180, null=True, verbose_name=b'通过日期'))]
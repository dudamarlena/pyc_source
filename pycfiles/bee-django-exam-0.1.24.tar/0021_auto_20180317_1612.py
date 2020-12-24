# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_exam/migrations/0021_auto_20180317_1612.py
# Compiled at: 2018-03-17 04:12:05
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_exam', '0020_auto_20180126_1410')]
    operations = [
     migrations.AlterField(model_name=b'notice', name=b'context', field=models.TextField(null=True, verbose_name=b'须知内容'))]
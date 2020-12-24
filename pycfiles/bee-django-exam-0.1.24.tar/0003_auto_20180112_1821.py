# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_exam/migrations/0003_auto_20180112_1821.py
# Compiled at: 2018-01-12 05:21:55
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_exam', '0002_auto_20180112_1812')]
    operations = [
     migrations.AlterField(model_name=b'notice', name=b'title', field=models.CharField(max_length=180, verbose_name=b'须知标题'))]
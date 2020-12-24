# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0035_auto_20190923_1715.py
# Compiled at: 2019-09-23 05:15:56
from __future__ import unicode_literals
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0034_auto_20190923_1715')]
    operations = [
     migrations.AlterField(model_name=b'userleaverecord', name=b'created_at', field=models.DateTimeField(default=django.utils.timezone.now))]
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_track/migrations/0002_auto_20180810_1846.py
# Compiled at: 2018-08-10 06:46:09
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_track', '0001_initial')]
    operations = [
     migrations.AlterField(model_name=b'usertrackrecord', name=b'info', field=models.TextField(blank=True, null=True, verbose_name=b'详情'))]
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_track/migrations/0007_auto_20190918_1510.py
# Compiled at: 2019-09-18 03:10:45
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_track', '0006_auto_20181109_1336')]
    operations = [
     migrations.AlterField(model_name=b'usertrackrecord', name=b'content_id', field=models.IntegerField(null=True))]
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0016_auto_20190111_1554.py
# Compiled at: 2019-01-11 02:54:14
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0015_auto_20190110_1356')]
    operations = [
     migrations.AlterField(model_name=b'contract', name=b'duration', field=models.IntegerField(blank=True, help_text=b'如【周期】为【长期】，则不用填写此字段', null=True, verbose_name=b'时长')),
     migrations.AlterField(model_name=b'contract', name=b'period', field=models.IntegerField(verbose_name=b'周期'))]
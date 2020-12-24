# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_coin/migrations/0021_order_deliver.py
# Compiled at: 2019-11-06 02:29:40
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_coin', '0020_auto_20191106_1516')]
    operations = [
     migrations.AddField(model_name=b'order', name=b'deliver', field=models.TextField(blank=True, help_text=b'填写快递单号等信息', null=True, verbose_name=b'发货信息'))]
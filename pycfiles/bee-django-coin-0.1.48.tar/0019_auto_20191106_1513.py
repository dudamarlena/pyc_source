# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_coin/migrations/0019_auto_20191106_1513.py
# Compiled at: 2019-11-06 02:13:49
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_coin', '0018_auto_20191106_1513')]
    operations = [
     migrations.AlterField(model_name=b'order', name=b'info', field=models.TextField(blank=True, null=True, verbose_name=b'备注'))]
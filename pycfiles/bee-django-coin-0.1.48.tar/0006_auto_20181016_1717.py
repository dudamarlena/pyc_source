# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_coin/migrations/0006_auto_20181016_1717.py
# Compiled at: 2018-10-16 05:17:50
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_coin', '0005_auto_20181016_1619')]
    operations = [
     migrations.RemoveField(model_name=b'othercoincount', name=b'other_type'),
     migrations.AddField(model_name=b'othercoincount', name=b'coin_type', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=b'bee_django_coin.CoinType', verbose_name=b'类型'))]
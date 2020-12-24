# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_coin/migrations/0011_auto_20181109_1422.py
# Compiled at: 2018-11-09 01:22:56
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_coin', '0010_auto_20181109_1415')]
    operations = [
     migrations.RemoveField(model_name=b'item', name=b'stauts'),
     migrations.AddField(model_name=b'item', name=b'status', field=models.IntegerField(choices=[(1, '上架'), (2, '下架')], default=0, verbose_name=b'商品状态')),
     migrations.AlterField(model_name=b'item', name=b'item_type', field=models.IntegerField(choices=[(1, '实物'), (2, '抵用券')], default=0, verbose_name=b'商品类型'))]
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_coin/migrations/0016_auto_20181219_2057.py
# Compiled at: 2018-12-19 07:57:46
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_coin', '0015_auto_20181122_1337')]
    operations = [
     migrations.AlterModelOptions(name=b'item', options={b'ordering': [b'pk'], b'permissions': (('view_item_list', '查看商品列表'), )}),
     migrations.AlterModelOptions(name=b'order', options={b'ordering': [b'-created_at'], b'permissions': (('view_order_list', '查看订单列表'), )})]
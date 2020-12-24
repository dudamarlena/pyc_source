# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/orders/migrations/0005_auto_20190120_1724.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 444 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('orders', '0004_orderitem_is_tax')]
    operations = [
     migrations.AlterModelOptions(name='orderitem',
       options={'ordering':('created_at', ), 
      'verbose_name':'OrderItem',  'verbose_name_plural':'OrderItems'})]
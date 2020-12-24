# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/orders/migrations/0004_orderitem_is_tax.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 437 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('orders', '0003_order_address_obj')]
    operations = [
     migrations.AddField(model_name='orderitem',
       name='is_tax',
       field=models.BooleanField(default=False, verbose_name='Is Tax'))]
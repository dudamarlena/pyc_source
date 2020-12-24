# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/orders/migrations/0006_order_uuid.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 459 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('orders', '0005_auto_20190120_1724')]
    operations = [
     migrations.AddField(model_name='order',
       name='uuid',
       field=models.UUIDField(blank=True, editable=False, null=True, verbose_name='Reference ID'))]
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/orders/migrations/0008_auto_20190121_2101.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 483 bytes
from django.db import migrations, models
import uuid

class Migration(migrations.Migration):
    dependencies = [
     ('orders', '0007_auto_20190121_1856')]
    operations = [
     migrations.AlterField(model_name='order',
       name='uuid',
       field=models.UUIDField(default=(uuid.uuid4), editable=False, unique=True, verbose_name='Reference ID'))]
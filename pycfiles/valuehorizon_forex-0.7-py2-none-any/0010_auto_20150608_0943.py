# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/Development/customapps/valuehorizon-forex/forex/migrations/0010_auto_20150608_0943.py
# Compiled at: 2016-06-02 13:23:51
from __future__ import unicode_literals
from django.db import models, migrations
from decimal import Decimal
import django.core.validators

class Migration(migrations.Migration):
    dependencies = [
     ('forex', '0009_auto_20150529_1110')]
    operations = [
     migrations.AlterField(model_name=b'currencyprice', name=b'bid_price', field=models.DecimalField(default=0, max_digits=20, decimal_places=4, validators=[django.core.validators.MinValueValidator(Decimal(b'0.00'))]), preserve_default=False)]
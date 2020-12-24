# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/Development/customapps/valuehorizon-forex/forex/migrations/0007_auto_20150526_1255.py
# Compiled at: 2016-06-02 13:23:51
from __future__ import unicode_literals
from django.db import models, migrations
from decimal import Decimal
import django.core.validators

class Migration(migrations.Migration):
    dependencies = [
     ('forex', '0006_auto_20150524_1013')]
    operations = [
     migrations.AlterField(model_name=b'currencyprices', name=b'ask_price', field=models.DecimalField(max_digits=20, decimal_places=4, validators=[django.core.validators.MinValueValidator(Decimal(b'0.00'))])),
     migrations.AlterField(model_name=b'currencyprices', name=b'bid_price', field=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=4, validators=[django.core.validators.MinValueValidator(Decimal(b'0.00'))]))]
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/Development/customapps/valuehorizon-forex/forex/migrations/0003_auto_20150508_1447.py
# Compiled at: 2016-06-02 13:23:51
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('forex', '0002_auto_20150508_1326')]
    operations = [
     migrations.AlterField(model_name=b'currencyprices', name=b'ask_price_us', field=models.DecimalField(default=0, editable=False, max_digits=20, decimal_places=4), preserve_default=False),
     migrations.AlterField(model_name=b'currencyprices', name=b'bid_price_us', field=models.DecimalField(default=0, editable=False, max_digits=20, decimal_places=4), preserve_default=False)]
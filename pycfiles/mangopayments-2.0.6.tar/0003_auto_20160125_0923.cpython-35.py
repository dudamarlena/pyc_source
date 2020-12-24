# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/polona/Olaii/Olaii_Mangopayments/olaii-mangopay/mangopayments/migrations/0003_auto_20160125_0923.py
# Compiled at: 2017-09-14 03:07:11
# Size of source mod 2**32: 706 bytes
from __future__ import unicode_literals
from django.db import migrations, models
from decimal import Decimal

class Migration(migrations.Migration):
    dependencies = [
     ('mangopayments', '0002_mangopaypayin_result_message')]
    operations = [
     migrations.AddField(model_name='mangopayrefund', name='debited_funds', field=models.DecimalField(default=Decimal('0.0'), max_digits=12, decimal_places=2)),
     migrations.AddField(model_name='mangopayrefund', name='fees', field=models.DecimalField(default=Decimal('0.0'), max_digits=12, decimal_places=2))]
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/polona/Olaii/Olaii_Mangopayments/olaii-mangopay/mangopayments/migrations/0017_auto_20171215_1310.py
# Compiled at: 2017-12-15 08:10:24
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('mangopayments', '0016_auto_20171215_1129')]
    operations = [
     migrations.AlterField(model_name=b'mangopaybankaccount', name=b'account_type', field=models.CharField(choices=[('IBAN', 'IBAN'), ('US', 'US'), ('OTHER', 'Other')], default=b'IBAN', max_length=5))]
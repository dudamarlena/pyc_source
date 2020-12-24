# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/polona/Olaii/Olaii_Mangopayments/olaii-mangopay/mangopayments/migrations/0018_auto_20171215_1353.py
# Compiled at: 2017-12-15 08:53:51
# Size of source mod 2**32: 549 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('mangopayments', '0017_auto_20171215_1310')]
    operations = [
     migrations.AlterField(model_name='mangopaybankaccount', name='account_type', field=models.CharField(choices=[(b'BI', 'IBAN'), (b'US', 'US'), (b'O', 'Other')], default=b'BI', max_length=5))]
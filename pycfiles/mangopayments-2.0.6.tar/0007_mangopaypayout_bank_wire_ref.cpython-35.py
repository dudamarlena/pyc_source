# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/polona/Olaii/Olaii_Mangopayments/olaii-mangopay/mangopayments/migrations/0007_mangopaypayout_bank_wire_ref.py
# Compiled at: 2017-09-14 03:07:11
# Size of source mod 2**32: 469 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('mangopayments', '0006_mangopaybankaccount_owner_name')]
    operations = [
     migrations.AddField(model_name='mangopaypayout', name='bank_wire_ref', field=models.CharField(default=b'', max_length=12, null=True, blank=True))]
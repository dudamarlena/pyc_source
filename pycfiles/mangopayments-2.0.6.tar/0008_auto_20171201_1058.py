# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/polona/Olaii/Olaii_Mangopayments/olaii-mangopay/mangopayments/migrations/0008_auto_20171201_1058.py
# Compiled at: 2017-12-08 08:13:34
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('mangopayments', '0007_mangopaypayout_bank_wire_ref')]
    operations = [
     migrations.AlterField(model_name=b'mangopayuser', name=b'type', field=models.CharField(choices=[('N', 'Natural User'), ('B', 'BUSINESS'), ('O', 'ORGANIZATION'), ('S', 'SOLETRADER')], max_length=1, null=True))]
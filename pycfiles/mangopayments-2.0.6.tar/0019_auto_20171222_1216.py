# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/polona/Olaii/Olaii_Mangopayments/olaii-mangopay/mangopayments/migrations/0019_auto_20171222_1216.py
# Compiled at: 2017-12-22 07:16:35
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('mangopayments', '0018_auto_20171215_1353')]
    operations = [
     migrations.AlterField(model_name=b'mangopaydocument', name=b'status', field=models.CharField(blank=True, choices=[('CREATED', 'CREATED'), ('VALIDATION_ASKED', 'VALIDATION ASKED'), ('VALIDATED', 'VALIDATED'), ('REFUSED', 'REFUSED')], max_length=1, null=True)),
     migrations.AlterField(model_name=b'mangopaydocument', name=b'type', field=models.CharField(choices=[('IDENTITY_PROOF', 'IDENTITY PROOF'), ('REGISTRATION_PROOF', 'REGISTRATION PROOF'), ('ARTICLES_OF_ASSOCIATION', 'ARTICLES OF ASSOCIATION'), ('SHAREHOLDER_DECLARATION', 'SHAREHOLDER DECLARATION'), ('ADDRESS_PROOF', 'ADDRESS PROOF')], max_length=2))]
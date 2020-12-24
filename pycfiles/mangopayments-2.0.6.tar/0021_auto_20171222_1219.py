# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/polona/Olaii/Olaii_Mangopayments/olaii-mangopay/mangopayments/migrations/0021_auto_20171222_1219.py
# Compiled at: 2017-12-22 07:19:48
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('mangopayments', '0020_auto_20171222_1217')]
    operations = [
     migrations.AlterField(model_name=b'mangopaydocument', name=b'status', field=models.CharField(blank=True, choices=[('CREATED', 'CREATED'), ('VALIDATION_ASKED', 'VALIDATION_ASKED'), ('VALIDATED', 'VALIDATED'), ('REFUSED', 'REFUSED')], max_length=25, null=True)),
     migrations.AlterField(model_name=b'mangopaydocument', name=b'type', field=models.CharField(choices=[('IDENTITY_PROOF', 'IDENTITY_PROOF'), ('REGISTRATION_PROOF', 'REGISTRATION_PROOF'), ('ARTICLES_OF_ASSOCIATION', 'ARTICLES_OF_ASSOCIATION'), ('SHAREHOLDER_DECLARATION', 'SHAREHOLDER_DECLARATION'), ('ADDRESS_PROOF', 'ADDRESS_PROOF')], max_length=25))]
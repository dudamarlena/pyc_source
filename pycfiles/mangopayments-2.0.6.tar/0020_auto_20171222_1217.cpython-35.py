# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/polona/Olaii/Olaii_Mangopayments/olaii-mangopay/mangopayments/migrations/0020_auto_20171222_1217.py
# Compiled at: 2017-12-22 07:17:39
# Size of source mod 2**32: 1039 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('mangopayments', '0019_auto_20171222_1216')]
    operations = [
     migrations.AlterField(model_name='mangopaydocument', name='status', field=models.CharField(blank=True, choices=[(b'CREATED', b'CREATED'), (b'VALIDATION_ASKED', b'VALIDATION ASKED'), (b'VALIDATED', b'VALIDATED'), (b'REFUSED', b'REFUSED')], max_length=25, null=True)),
     migrations.AlterField(model_name='mangopaydocument', name='type', field=models.CharField(choices=[(b'IDENTITY_PROOF', b'IDENTITY PROOF'), (b'REGISTRATION_PROOF', b'REGISTRATION PROOF'), (b'ARTICLES_OF_ASSOCIATION', b'ARTICLES OF ASSOCIATION'), (b'SHAREHOLDER_DECLARATION', b'SHAREHOLDER DECLARATION'), (b'ADDRESS_PROOF', b'ADDRESS PROOF')], max_length=25))]
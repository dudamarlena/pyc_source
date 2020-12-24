# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/polona/Olaii/Olaii_Mangopayments/olaii-mangopay/mangopayments/migrations/0021_auto_20171222_1219.py
# Compiled at: 2017-12-22 07:19:48
# Size of source mod 2**32: 1039 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('mangopayments', '0020_auto_20171222_1217')]
    operations = [
     migrations.AlterField(model_name='mangopaydocument', name='status', field=models.CharField(blank=True, choices=[(b'CREATED', b'CREATED'), (b'VALIDATION_ASKED', b'VALIDATION_ASKED'), (b'VALIDATED', b'VALIDATED'), (b'REFUSED', b'REFUSED')], max_length=25, null=True)),
     migrations.AlterField(model_name='mangopaydocument', name='type', field=models.CharField(choices=[(b'IDENTITY_PROOF', b'IDENTITY_PROOF'), (b'REGISTRATION_PROOF', b'REGISTRATION_PROOF'), (b'ARTICLES_OF_ASSOCIATION', b'ARTICLES_OF_ASSOCIATION'), (b'SHAREHOLDER_DECLARATION', b'SHAREHOLDER_DECLARATION'), (b'ADDRESS_PROOF', b'ADDRESS_PROOF')], max_length=25))]
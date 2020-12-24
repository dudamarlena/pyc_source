# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/polona/Olaii/Olaii_Mangopayments/olaii-mangopay/mangopayments/migrations/0014_auto_20171207_1024.py
# Compiled at: 2017-12-08 08:13:34
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('mangopayments', '0013_mangopaytransfer_result_message')]
    operations = [
     migrations.AddField(model_name=b'mangopaypayout', name=b'result_code', field=models.CharField(blank=True, max_length=6, null=True)),
     migrations.AddField(model_name=b'mangopaypayout', name=b'result_message', field=models.CharField(blank=True, max_length=255, null=True))]
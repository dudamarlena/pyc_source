# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/polona/Olaii/Olaii_Mangopayments/olaii-mangopay/mangopayments/migrations/0002_mangopaypayin_result_message.py
# Compiled at: 2017-09-14 03:07:11
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('mangopayments', '0001_initial')]
    operations = [
     migrations.AddField(model_name=b'mangopaypayin', name=b'result_message', field=models.CharField(max_length=255, null=True, blank=True))]
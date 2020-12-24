# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/polona/Olaii/Olaii_Mangopayments/olaii-mangopay/mangopayments/migrations/0013_mangopaytransfer_result_message.py
# Compiled at: 2017-12-08 08:13:34
# Size of source mod 2**32: 497 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('mangopayments', '0012_auto_20171206_1524')]
    operations = [
     migrations.AddField(model_name='mangopaytransfer', name='result_message', field=models.CharField(blank=True, max_length=256, null=True))]
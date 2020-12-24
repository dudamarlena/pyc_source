# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/polona/Olaii/Olaii_Mangopayments/olaii-mangopay/mangopayments/migrations/0015_auto_20171207_1321.py
# Compiled at: 2017-12-08 08:13:34
# Size of source mod 2**32: 674 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('mangopayments', '0014_auto_20171207_1024')]
    operations = [
     migrations.AddField(model_name='mangopayrefund', name='execution_date', field=models.DateTimeField(blank=True, null=True)),
     migrations.AddField(model_name='mangopayrefund', name='result_message', field=models.CharField(blank=True, max_length=255, null=True))]
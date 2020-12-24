# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/polona/Olaii/Olaii_Mangopayments/olaii-mangopay/mangopayments/migrations/0006_mangopaybankaccount_owner_name.py
# Compiled at: 2017-09-14 03:07:11
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('mangopayments', '0005_auto_20160311_1342')]
    operations = [
     migrations.AddField(model_name=b'mangopaybankaccount', name=b'owner_name', field=models.CharField(default=b'', max_length=255))]
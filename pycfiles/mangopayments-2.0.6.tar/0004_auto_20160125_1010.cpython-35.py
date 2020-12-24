# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/polona/Olaii/Olaii_Mangopayments/olaii-mangopay/mangopayments/migrations/0004_auto_20160125_1010.py
# Compiled at: 2017-09-14 03:07:11
# Size of source mod 2**32: 728 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('mangopayments', '0003_auto_20160125_0923')]
    operations = [
     migrations.RemoveField(model_name='mangopayrefund', name='execution_date'),
     migrations.AddField(model_name='mangopayrefund', name='created', field=models.DateTimeField(auto_now_add=True, null=True)),
     migrations.AddField(model_name='mangopayrefund', name='updated', field=models.DateTimeField(auto_now=True, null=True))]
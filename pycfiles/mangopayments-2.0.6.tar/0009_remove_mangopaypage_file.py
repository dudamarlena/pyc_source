# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/polona/Olaii/Olaii_Mangopayments/olaii-mangopay/mangopayments/migrations/0009_remove_mangopaypage_file.py
# Compiled at: 2017-12-08 08:13:34
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('mangopayments', '0008_auto_20171201_1058')]
    operations = [
     migrations.RemoveField(model_name=b'mangopaypage', name=b'file')]
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/Development/customapps/valuehorizon-forex/forex/migrations/0009_auto_20150529_1110.py
# Compiled at: 2016-06-02 13:23:51
from __future__ import unicode_literals
from django.db import models, migrations
from decimal import Decimal
import django.core.validators

class Migration(migrations.Migration):
    dependencies = [
     ('forex', '0008_auto_20150526_1310')]
    operations = [
     migrations.RenameModel(old_name=b'CurrencyPrices', new_name=b'CurrencyPrice')]
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/Development/customapps/valuehorizon-forex/forex/migrations/0006_auto_20150524_1013.py
# Compiled at: 2016-06-02 13:23:51
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('forex', '0005_auto_20150522_1402')]
    operations = [
     migrations.RemoveField(model_name=b'currencyprices', name=b'ask_price_us'),
     migrations.RemoveField(model_name=b'currencyprices', name=b'bid_price_us')]
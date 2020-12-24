# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/Development/customapps/valuehorizon-forex/forex/migrations/0004_auto_20150508_1504.py
# Compiled at: 2016-06-02 13:23:51
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('forex', '0003_auto_20150508_1447')]
    operations = [
     migrations.RemoveField(model_name=b'currency', name=b'change_52_week'),
     migrations.RemoveField(model_name=b'currency', name=b'latest_ask_price'),
     migrations.RemoveField(model_name=b'currency', name=b'latest_ask_price_us'),
     migrations.RemoveField(model_name=b'currency', name=b'latest_change'),
     migrations.RemoveField(model_name=b'currency', name=b'latest_date'),
     migrations.RemoveField(model_name=b'currency', name=b'volatility_52_week')]
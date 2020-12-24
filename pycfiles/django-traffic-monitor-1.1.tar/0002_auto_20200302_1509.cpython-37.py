# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/genonfire/git/gencode/traffic_monitor/migrations/0002_auto_20200302_1509.py
# Compiled at: 2020-03-02 01:09:25
# Size of source mod 2**32: 541 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('traffic_monitor', '0001_initial')]
    operations = [
     migrations.AddField(model_name='traffic',
       name='rx_read',
       field=models.BigIntegerField(default=0)),
     migrations.AddField(model_name='traffic',
       name='tx_read',
       field=models.BigIntegerField(default=0))]
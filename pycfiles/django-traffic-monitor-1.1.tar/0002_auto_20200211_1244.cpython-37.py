# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/genonfire/git/gencode/traffic_monitor/migrations/0002_auto_20200211_1244.py
# Compiled at: 2020-02-10 22:44:07
# Size of source mod 2**32: 517 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('traffic_monitor', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name='traffic',
       options={'ordering': ('-date', '-id')}),
     migrations.AddField(model_name='traffic',
       name='init_data',
       field=models.BooleanField(default=False))]
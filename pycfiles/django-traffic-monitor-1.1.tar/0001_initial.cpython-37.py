# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/genonfire/git/gencode/traffic_monitor/migrations/0001_initial.py
# Compiled at: 2020-03-02 00:59:24
# Size of source mod 2**32: 947 bytes
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Traffic',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'interface', models.CharField(max_length=254)),
      (
       'rx_bytes', models.BigIntegerField(default=0)),
      (
       'tx_bytes', models.BigIntegerField(default=0)),
      (
       'date', models.DateField(unique=True)),
      (
       'updated_at', models.DateTimeField(default=(django.utils.timezone.now))),
      (
       'init_data', models.BooleanField(default=False))],
       options={'ordering': ('-date', '-id')})]
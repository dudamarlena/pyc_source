# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/migrations/0007_add_argon2_with_rolling_upgrades.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 963 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('delivery', '0006_report_autosaved')]
    operations = [
     migrations.AddField(model_name='matchreport',
       name='encode_prefix',
       field=models.CharField(max_length=500, blank=True)),
     migrations.AddField(model_name='report',
       name='encode_prefix',
       field=models.CharField(max_length=500, blank=True)),
     migrations.AlterField(model_name='matchreport',
       name='salt',
       field=models.CharField(max_length=256, blank=False)),
     migrations.AlterField(model_name='report',
       name='salt',
       field=models.CharField(max_length=256, blank=False))]
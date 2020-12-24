# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jojo/workspace/locations/src/unicef_locations/migrations/0005_auto_20181206_1127.py
# Compiled at: 2019-04-19 21:07:17
# Size of source mod 2**32: 431 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('locations', '0004_pcode_remap_related')]
    operations = [
     migrations.AlterField(model_name='location',
       name='is_active',
       field=models.BooleanField(blank=True, default=True, verbose_name='Active'))]
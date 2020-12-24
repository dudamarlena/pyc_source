# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jojo/workspace/locations/src/unicef_locations/migrations/0007_auto_20190122_1428.py
# Compiled at: 2019-04-19 21:07:20
# Size of source mod 2**32: 421 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('locations', '0006_auto_20190110_2336')]
    operations = [
     migrations.AlterModelOptions(name='locationremaphistory',
       options={'verbose_name':'Remap history', 
      'verbose_name_plural':'Location remap history'})]
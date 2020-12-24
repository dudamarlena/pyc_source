# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jojo/workspace/locations/src/unicef_locations/migrations/0003_make_not_nullable.py
# Compiled at: 2019-04-19 21:07:17
# Size of source mod 2**32: 1168 bytes
from django.db import migrations, models
from unicef_locations.libs import get_random_color

class Migration(migrations.Migration):
    dependencies = [
     ('locations', '0002_fix_null_values')]
    operations = [
     migrations.AlterField(model_name='cartodbtable',
       name='color',
       field=models.CharField(blank=True,
       default=get_random_color,
       max_length=7,
       verbose_name='Color')),
     migrations.AlterField(model_name='cartodbtable',
       name='display_name',
       field=models.CharField(blank=True, default='', max_length=254, verbose_name='Display Name')),
     migrations.AlterField(model_name='cartodbtable',
       name='parent_code_col',
       field=models.CharField(blank=True, default='', max_length=254, verbose_name='Parent Code Column')),
     migrations.AlterField(model_name='location',
       name='p_code',
       field=models.CharField(blank=True, default='', max_length=32, verbose_name='P Code'))]
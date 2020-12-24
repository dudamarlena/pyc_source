# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_geodata/migrations/0003_auto_20180118_1209.py
# Compiled at: 2018-01-18 06:20:47
# Size of source mod 2**32: 607 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_geodata', '0002_auto_20170921_1206')]
    operations = [
     migrations.AlterField(model_name='city', name='time_zone', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='codenerix_geodata.TimeZone', verbose_name='Timezone'))]
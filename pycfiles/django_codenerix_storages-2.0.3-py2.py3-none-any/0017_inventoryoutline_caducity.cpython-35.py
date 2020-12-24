# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_storages/migrations/0017_inventoryoutline_caducity.py
# Compiled at: 2018-02-23 13:02:41
# Size of source mod 2**32: 519 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_storages', '0016_auto_20180223_1846')]
    operations = [
     migrations.AddField(model_name='inventoryoutline', name='caducity', field=models.DateField(blank=True, default=None, null=True, verbose_name='Caducity'))]
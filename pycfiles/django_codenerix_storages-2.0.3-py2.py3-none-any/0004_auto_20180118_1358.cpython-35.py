# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_storages/migrations/0004_auto_20180118_1358.py
# Compiled at: 2018-01-18 08:08:06
# Size of source mod 2**32: 515 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_storages', '0003_auto_20180118_1151')]
    operations = [
     migrations.AlterField(model_name='storageboxstructure', name='max_weight', field=models.FloatField(blank=True, null=True, verbose_name='Max weight'))]
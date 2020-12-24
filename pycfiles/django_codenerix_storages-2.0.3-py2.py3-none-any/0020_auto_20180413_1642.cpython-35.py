# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_storages/migrations/0020_auto_20180413_1642.py
# Compiled at: 2018-04-13 10:42:23
# Size of source mod 2**32: 886 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_storages', '0019_distribution_distributionline')]
    operations = [
     migrations.AddField(model_name='inventoryinline', name='notes', field=models.TextField(blank=True, null=True, verbose_name='Notes')),
     migrations.AddField(model_name='inventoryline', name='notes', field=models.TextField(blank=True, null=True, verbose_name='Notes')),
     migrations.AddField(model_name='inventoryoutline', name='notes', field=models.TextField(blank=True, null=True, verbose_name='Notes'))]
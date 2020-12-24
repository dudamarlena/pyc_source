# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_storages/migrations/0012_inventory_kind.py
# Compiled at: 2018-02-15 11:49:00
# Size of source mod 2**32: 573 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_storages', '0011_merge_20180202_0726')]
    operations = [
     migrations.AddField(model_name='inventory', name='kind', field=models.CharField(choices=[('B', 'Internal'), ('I', 'Input'), ('O', 'Output')], default='B', editable=False, max_length=1, verbose_name='Kind'))]
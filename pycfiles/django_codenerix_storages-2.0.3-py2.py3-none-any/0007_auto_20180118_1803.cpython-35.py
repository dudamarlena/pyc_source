# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_storages/migrations/0007_auto_20180118_1803.py
# Compiled at: 2018-01-18 12:03:54
# Size of source mod 2**32: 461 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_storages', '0006_auto_20180118_1724')]
    operations = [
     migrations.RenameField(model_name='inventoryalbaran', old_name='storage_operator', new_name='operator')]
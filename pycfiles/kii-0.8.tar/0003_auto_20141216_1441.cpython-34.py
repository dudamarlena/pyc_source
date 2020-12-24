# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/stream/migrations/0003_auto_20141216_1441.py
# Compiled at: 2015-01-17 16:40:50
# Size of source mod 2**32: 497 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('stream', '0002_auto_20141216_1106')]
    operations = [
     migrations.AlterModelOptions(name='streamitem', options={'ordering': ['-publication_date'],  'permissions': (('read', 'permissions.view'), ('write', 'permissions.edit'), ('delete', 'permissions.delete'))})]
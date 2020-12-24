# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_geodata/migrations/0002_auto_20170921_1206.py
# Compiled at: 2018-01-17 10:14:34
# Size of source mod 2**32: 2047 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_geodata', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name='citygeonameen', options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.AlterModelOptions(name='citygeonamees', options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.AlterModelOptions(name='continentgeonameen', options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.AlterModelOptions(name='continentgeonamees', options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.AlterModelOptions(name='countrygeonameen', options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.AlterModelOptions(name='countrygeonamees', options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.AlterModelOptions(name='provincegeonameen', options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.AlterModelOptions(name='provincegeonamees', options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.AlterModelOptions(name='regiongeonameen', options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.AlterModelOptions(name='regiongeonamees', options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')})]
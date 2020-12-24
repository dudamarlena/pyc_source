# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_cms/migrations/0007_auto_20171115_1546.py
# Compiled at: 2017-11-28 07:16:52
# Size of source mod 2**32: 2066 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_cms', '0006_auto_20171108_1628')]
    operations = [
     migrations.AlterModelOptions(name='slider', options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.AlterModelOptions(name='sliderelement', options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.AlterModelOptions(name='sliderelementtexten', options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.AlterModelOptions(name='sliderelementtextes', options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.AlterModelOptions(name='staticheader', options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.AlterModelOptions(name='staticheaderelement', options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.AlterModelOptions(name='staticheaderelementtexten', options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.AlterModelOptions(name='staticheaderelementtextes', options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.AlterModelOptions(name='staticpagetexten', options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.AlterModelOptions(name='staticpagetextes', options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')})]
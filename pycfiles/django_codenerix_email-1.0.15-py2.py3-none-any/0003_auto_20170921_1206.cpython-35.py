# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_email/migrations/0003_auto_20170921_1206.py
# Compiled at: 2017-09-21 12:09:51
# Size of source mod 2**32: 656 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_email', '0002_auto_20170502_1043')]
    operations = [
     migrations.AlterModelOptions(name='emailtemplatetexten', options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.AlterModelOptions(name='emailtemplatetextes', options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')})]
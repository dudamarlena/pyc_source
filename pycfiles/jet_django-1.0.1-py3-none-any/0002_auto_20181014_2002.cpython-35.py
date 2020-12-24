# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_django/jet_django/migrations/0002_auto_20181014_2002.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 761 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('jet_django', '0001_initial')]
    operations = [
     migrations.DeleteModel(name='MenuSettings'),
     migrations.DeleteModel(name='ModelDescription'),
     migrations.DeleteModel(name='ViewSettings'),
     migrations.RemoveField(model_name='widget', name='dashboard'),
     migrations.DeleteModel(name='Dashboard'),
     migrations.DeleteModel(name='Widget')]
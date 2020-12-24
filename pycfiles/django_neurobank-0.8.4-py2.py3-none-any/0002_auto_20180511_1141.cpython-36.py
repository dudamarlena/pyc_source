# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmeliza/Devel/django-neurobank/neurobank/migrations/0002_auto_20180511_1141.py
# Compiled at: 2018-05-11 11:52:24
# Size of source mod 2**32: 668 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('neurobank', '0001_initial')]
    operations = [
     migrations.RenameModel(old_name='Domain',
       new_name='Archive'),
     migrations.RenameField(model_name='location',
       old_name='domain',
       new_name='archive'),
     migrations.AlterUniqueTogether(name='location',
       unique_together=(set([('resource', 'archive')])))]
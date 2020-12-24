# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/banlist/migrations/0002_auto_20181114_2144.py
# Compiled at: 2019-04-03 22:56:25
# Size of source mod 2**32: 475 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('banlist', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='bannedperson',
       name='lastName',
       field=models.CharField(max_length=30, verbose_name='Last name'))]
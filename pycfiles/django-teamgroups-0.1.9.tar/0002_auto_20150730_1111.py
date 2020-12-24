# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sbarnett/Dropbox/Dev/Django/the_cake_club/teamgroups/migrations/0002_auto_20150730_1111.py
# Compiled at: 2015-07-30 07:11:04
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('teamgroups', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name=b'teamgroup', options={b'permissions': (('view_teamgroup', 'Can view teamgroup'), ('leave_teamgroup', 'Can leave teamgroup'))})]
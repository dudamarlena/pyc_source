# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmeliza/Devel/django-neurobank/neurobank/migrations/0002_auto_20180206_2108.py
# Compiled at: 2018-02-06 21:08:19
# Size of source mod 2**32: 414 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('neurobank', '0001_initial')]
    operations = [
     migrations.AlterUniqueTogether(name='domain', unique_together=set([('scheme', 'root')]))]
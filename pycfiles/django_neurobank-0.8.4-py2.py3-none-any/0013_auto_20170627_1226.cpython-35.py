# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmeliza/Devel/django-neurobank/neurobank/migrations/0013_auto_20170627_1226.py
# Compiled at: 2017-06-27 12:26:34
# Size of source mod 2**32: 431 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('neurobank', '0012_auto_20170627_1049')]
    operations = [
     migrations.AlterUniqueTogether(name='location', unique_together=set([('resource', 'domain')]))]
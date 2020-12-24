# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gkarak/workspace/python/aluminium/ninecms/migrations/0006_auto_20150701_1401.py
# Compiled at: 2015-07-01 07:01:35
# Size of source mod 2**32: 620 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('ninecms', '0005_auto_20150624_1841')]
    operations = [
     migrations.AddField(model_name='pagelayoutelement', name='hidden', field=models.BooleanField(db_index=True, default=False)),
     migrations.AlterField(model_name='node', name='language', field=models.CharField(max_length=2, blank=True, choices=[('el', 'Greek')]))]
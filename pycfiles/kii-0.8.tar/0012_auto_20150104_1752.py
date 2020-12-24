# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/stream/migrations/0012_auto_20150104_1752.py
# Compiled at: 2015-01-18 07:28:37
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('stream', '0011_auto_20150104_1751')]
    operations = [
     migrations.AlterUniqueTogether(name=b'stream', unique_together=None)]
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/migrations/0020_remove_matchreport_seen.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 332 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('delivery', '0019_auto_20171119_1543')]
    operations = [
     migrations.RemoveField(model_name='matchreport', name='seen')]
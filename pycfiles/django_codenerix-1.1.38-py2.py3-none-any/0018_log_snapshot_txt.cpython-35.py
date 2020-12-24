# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix/migrations/0018_log_snapshot_txt.py
# Compiled at: 2017-12-18 07:03:26
# Size of source mod 2**32: 481 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix', '0017_auto_20170428_0850')]
    operations = [
     migrations.AddField(model_name='log', name='snapshot_txt', field=models.TextField(blank=True, verbose_name=b'Snapshot Txt'))]
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/migrations/0015_matchreport_identifier.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 471 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('delivery', '0014_report_contact_notes')]
    operations = [
     migrations.AlterField(model_name='matchreport',
       name='identifier',
       field=models.CharField(blank=True, max_length=500, null=True))]
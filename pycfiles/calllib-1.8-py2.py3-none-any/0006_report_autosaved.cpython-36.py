# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/migrations/0006_report_autosaved.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 474 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('delivery', '0005_delete_encrypted_fields_from_match_report')]
    operations = [
     migrations.AddField(model_name='report',
       name='autosaved',
       field=models.BooleanField(default=False, null=False))]
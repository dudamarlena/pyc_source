# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/migrations/0011_report_uuid.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 437 bytes
from __future__ import unicode_literals
import uuid
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('delivery', '0010_email_notification_data_migration')]
    operations = [
     migrations.AddField(model_name='report',
       name='uuid',
       field=models.UUIDField(default=(uuid.uuid4)))]
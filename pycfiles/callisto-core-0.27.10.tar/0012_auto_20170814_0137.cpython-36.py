# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/migrations/0012_auto_20170814_0137.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 628 bytes
from __future__ import unicode_literals
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('delivery', '0011_report_uuid')]
    operations = [
     migrations.AlterField(model_name='report',
       name='owner',
       field=models.ForeignKey(null=True,
       on_delete=(django.db.models.deletion.CASCADE),
       to=(settings.AUTH_USER_MODEL)))]
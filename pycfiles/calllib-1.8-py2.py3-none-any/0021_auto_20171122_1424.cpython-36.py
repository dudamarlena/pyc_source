# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/migrations/0021_auto_20171122_1424.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 1186 bytes
from __future__ import unicode_literals
import django.utils.timezone
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('delivery', '0020_remove_matchreport_seen')]
    operations = [
     migrations.AddField(model_name='sentfullreport',
       name='new_sent',
       field=models.DateTimeField(auto_now_add=True,
       default=(django.utils.timezone.now)),
       preserve_default=False),
     migrations.AddField(model_name='sentfullreport',
       name='new_to_address',
       field=models.TextField(null=True)),
     migrations.AddField(model_name='sentmatchreport',
       name='new_sent',
       field=models.DateTimeField(auto_now_add=True,
       default=(django.utils.timezone.now)),
       preserve_default=False),
     migrations.AddField(model_name='sentmatchreport',
       name='new_to_address',
       field=models.TextField(null=True))]
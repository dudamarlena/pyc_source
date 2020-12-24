# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/migrations/0039_auto_20171208_0039.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 494 bytes
import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('delivery', '0038_uuid_unique_constraint')]
    operations = [
     migrations.AlterField(model_name='matchreport',
       name='report',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE),
       to='delivery.Report'))]
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
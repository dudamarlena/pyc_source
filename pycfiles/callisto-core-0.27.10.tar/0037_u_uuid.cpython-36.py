# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/migrations/0037_u_uuid.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 616 bytes
from __future__ import unicode_literals
import uuid
from django.db import migrations

def copy_attrs(apps, schema_editor):
    current_database = schema_editor.connection.alias
    Report = apps.get_model('delivery.Report')
    for row in Report.objects.using(current_database):
        row.uuid = uuid.uuid4()
        row.save()


class Migration(migrations.Migration):
    dependencies = [
     ('delivery', '0036_auto_20171122_1454')]
    operations = [
     migrations.RunPython(copy_attrs, reverse_code=(migrations.RunPython.noop))]
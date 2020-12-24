# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
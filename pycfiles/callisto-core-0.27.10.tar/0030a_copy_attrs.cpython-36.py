# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/migrations/0030a_copy_attrs.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 896 bytes
from __future__ import unicode_literals
from django.db import migrations

def copy_attrs(apps, schema_editor):
    current_database = schema_editor.connection.alias
    SentFullReport = apps.get_model('delivery.SentMatchReport')
    NewSentMatchReport = apps.get_model('delivery.NewSentMatchReport')
    for instance in SentFullReport.objects.using(current_database):
        new_instance = NewSentMatchReport.objects.create(sent=(instance.sent),
          to_address=(instance.to_address))
        for report in instance.reports.all():
            new_instance.reports.add(report)


class Migration(migrations.Migration):
    dependencies = [
     ('delivery', '0030_newsentmatchreport_proxysentmatchreport')]
    operations = [
     migrations.RunPython(copy_attrs, reverse_code=(migrations.RunPython.noop))]
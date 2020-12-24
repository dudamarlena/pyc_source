# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/migrations/0021a_copy_attrs.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 839 bytes
from __future__ import unicode_literals
from django.db import migrations

def _copy_attrs_for_instances(instances):
    for instance in instances:
        instance.new_sent = instance.sent
        instance.new_to_address = instance.to_address
        instance.save()


def copy_attrs(apps, schema_editor):
    current_database = schema_editor.connection.alias
    [_copy_attrs_for_instances(apps.get_model(f"delivery.{Name}").objects.using(current_database)) for Name in ('SentFullReport',
                                                                                                                'SentMatchReport')]


class Migration(migrations.Migration):
    dependencies = [
     ('delivery', '0021_auto_20171122_1424')]
    operations = [
     migrations.RunPython(copy_attrs, reverse_code=(migrations.RunPython.noop))]
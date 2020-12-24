# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Work/dev/cadasta/django-jsonattrs/jsonattrs/migrations/0004_convert_multilingual_fields.py
# Compiled at: 2017-01-30 12:18:04
# Size of source mod 2**32: 1399 bytes
from __future__ import unicode_literals
from django.db import migrations

def convert_attribute_long_names(apps, schema_editor):
    AttributeType = apps.get_model('jsonattrs', 'AttributeType')
    Attribute = apps.get_model('jsonattrs', 'Attribute')
    if not AttributeType.objects.exists():
        return
    for attr in Attribute.objects.all():
        attr.long_name_xlat = attr.long_name
        attr.save()


def convert_choice_labels(apps, schema_editor):
    AttributeType = apps.get_model('jsonattrs', 'AttributeType')
    Attribute = apps.get_model('jsonattrs', 'Attribute')
    if not AttributeType.objects.exists():
        return
    for attr in Attribute.objects.all():
        attr.choice_labels_xlat = attr.choice_labels
        attr.save()


class Migration(migrations.Migration):
    dependencies = [
     ('jsonattrs', '0003_prepare_multilingual_setup')]
    operations = [
     migrations.RunPython(code=convert_attribute_long_names, reverse_code=migrations.operations.special.RunPython.noop),
     migrations.RunPython(code=convert_choice_labels, reverse_code=migrations.operations.special.RunPython.noop)]
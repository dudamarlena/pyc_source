# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/migrations/0015_manual_20171121_0323.py
# Compiled at: 2017-11-28 02:59:59
from __future__ import unicode_literals
from django.db import migrations
from formfactory import SETTINGS

def update_fields_and_widgets(apps, schema_editor):
    fields = {}
    for field_type, name in SETTINGS[b'field-types']:
        fields[name] = field_type

    widgets = {}
    for widget_type, name in SETTINGS[b'widget-types']:
        widgets[name] = widget_type

    form_fields = apps.get_model(b'formfactory', b'FormField')
    for field in form_fields.objects.all():
        if field.field_type:
            field.field_type = fields[field.field_type]
        if field.widget:
            field.widget = widgets[field.widget]
        field.save()


class Migration(migrations.Migration):
    dependencies = [
     ('formfactory', '0014_auto_20171127_0206')]
    operations = [
     migrations.RunPython(update_fields_and_widgets)]
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/migrations/0005_added_enum_generic_relation.py
# Compiled at: 2017-09-07 07:30:48
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('contenttypes', '0002_remove_content_type_name'),
     ('formfactory', '0004_remove_form_post_to')]
    operations = [
     migrations.AddField(model_name=b'formfield', name=b'model_choices_content_type', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=b'contenttypes.ContentType')),
     migrations.AddField(model_name=b'formfield', name=b'model_choices_object_id', field=models.PositiveIntegerField(blank=True, null=True))]
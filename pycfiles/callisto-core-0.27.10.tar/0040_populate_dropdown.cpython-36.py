# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0040_populate_dropdown.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 672 bytes
from __future__ import unicode_literals
from django.db import migrations, models

def add_dropdowns(apps, schema_editor):
    current_database = schema_editor.connection.alias
    Question = apps.get_model('wizard_builder.FormQuestion')
    questions = Question.objects.filter(is_dropdown=True).using(current_database)
    for question in questions:
        question.type = 'dropdown'
        question.save()


class Migration(migrations.Migration):
    dependencies = [
     ('wizard_builder', '0039_dropdown_proxy')]
    operations = [
     migrations.RunPython(add_dropdowns, migrations.RunPython.noop)]
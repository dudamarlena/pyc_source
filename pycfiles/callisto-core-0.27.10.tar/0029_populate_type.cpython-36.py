# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0029_populate_type.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 918 bytes
from __future__ import unicode_literals
from django.db import migrations, models

def add_questions(apps, schema_editor):
    current_database = schema_editor.connection.alias
    QuestionSubmodels = [
     apps.get_model('wizard_builder.SingleLineText'),
     apps.get_model('wizard_builder.TextArea'),
     apps.get_model('wizard_builder.RadioButton'),
     apps.get_model('wizard_builder.Checkbox')]
    for Model in QuestionSubmodels:
        for question in Model.objects.using(current_database):
            question_type = question._meta.model_name.lower()
            question.type = question_type
            question.save()


class Migration(migrations.Migration):
    dependencies = [
     ('wizard_builder', '0028_formquestion_type')]
    operations = [
     migrations.RunPython(add_questions, migrations.RunPython.noop)]
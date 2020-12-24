# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
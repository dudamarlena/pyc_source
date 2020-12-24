# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0032_move_question_dropdown.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 981 bytes
from __future__ import unicode_literals
from django.db import migrations, models

def move_dropdown(apps, schema_editor):
    current_database = schema_editor.connection.alias
    RadioButton = apps.get_model('wizard_builder.RadioButton')
    for radiobutton in RadioButton.objects.using(current_database):
        formquestion = radiobutton.formquestion_ptr
        formquestion.is_dropdown = radiobutton.is_dropdown
        formquestion.save()


class Migration(migrations.Migration):
    dependencies = [
     ('wizard_builder', '0031_formquestion_choices_default')]
    operations = [
     migrations.AddField(model_name='formquestion',
       name='is_dropdown',
       field=models.BooleanField(default=False)),
     migrations.RunPython(move_dropdown, migrations.RunPython.noop),
     migrations.RemoveField(model_name='radiobutton', name='is_dropdown')]
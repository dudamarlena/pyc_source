# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
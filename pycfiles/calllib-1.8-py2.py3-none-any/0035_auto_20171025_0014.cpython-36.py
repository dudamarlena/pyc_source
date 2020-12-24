# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0035_auto_20171025_0014.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 964 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('wizard_builder', '0034e_move_choice_question')]
    operations = [
     migrations.RemoveField(model_name='checkbox', name='multiplechoice_ptr'),
     migrations.RemoveField(model_name='multiplechoice', name='formquestion_ptr'),
     migrations.RemoveField(model_name='radiobutton', name='multiplechoice_ptr'),
     migrations.RemoveField(model_name='singlelinetext', name='formquestion_ptr'),
     migrations.RemoveField(model_name='textarea', name='formquestion_ptr'),
     migrations.DeleteModel(name='Checkbox'),
     migrations.DeleteModel(name='MultipleChoice'),
     migrations.DeleteModel(name='RadioButton'),
     migrations.DeleteModel(name='SingleLineText'),
     migrations.DeleteModel(name='TextArea')]
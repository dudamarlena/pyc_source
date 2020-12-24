# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0034b_move_choice_question.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 662 bytes
from __future__ import unicode_literals
import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('wizard_builder', '0034a_move_choice_question')]
    operations = [
     migrations.AlterField(model_name='choice',
       name='question',
       field=models.ForeignKey(null=True,
       on_delete=(django.db.models.deletion.CASCADE),
       related_name='example1',
       to='wizard_builder.MultipleChoice'))]
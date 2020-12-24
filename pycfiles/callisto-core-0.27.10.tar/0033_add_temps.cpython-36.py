# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0033_add_temps.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 984 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('wizard_builder', '0032_move_question_dropdown')]
    operations = [
     migrations.AddField(model_name='checkbox',
       name='temp_04',
       field=models.TextField(null=True)),
     migrations.AddField(model_name='multiplechoice',
       name='temp_03',
       field=models.TextField(null=True)),
     migrations.AddField(model_name='radiobutton',
       name='temp_05',
       field=models.TextField(null=True)),
     migrations.AddField(model_name='singlelinetext',
       name='temp_01',
       field=models.TextField(null=True)),
     migrations.AddField(model_name='textarea',
       name='temp_02',
       field=models.TextField(null=True))]
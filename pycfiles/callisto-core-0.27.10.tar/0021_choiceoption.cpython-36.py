# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0021_choiceoption.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 1029 bytes
from __future__ import unicode_literals
import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('wizard_builder', '0020_choice_extra_info_text')]
    operations = [
     migrations.CreateModel(name='ChoiceOption',
       fields=[
      (
       'id',
       models.AutoField(auto_created=True,
         primary_key=True,
         serialize=False,
         verbose_name='ID')),
      (
       'text', models.TextField()),
      (
       'question',
       models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE),
         to='wizard_builder.Choice'))])]
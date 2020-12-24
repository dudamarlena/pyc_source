# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0039_dropdown_proxy.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 1165 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import callisto_core.wizard_builder.model_helpers

class Migration(migrations.Migration):
    dependencies = [
     ('wizard_builder', '0038_checkbox_radiobutton')]
    operations = [
     migrations.CreateModel(name='Dropdown',
       fields=[],
       options={'proxy':True, 
      'indexes':[]},
       bases=(
      callisto_core.wizard_builder.model_helpers.ProxyQuestion,
      'wizard_builder.formquestion')),
     migrations.AlterField(model_name='formquestion',
       name='type',
       field=models.TextField(choices=[
      ('checkbox', 'checkbox'),
      ('dropdown', 'dropdown'),
      ('radiobutton', 'radiobutton'),
      ('singlelinetext', 'singlelinetext'),
      ('textarea', 'textarea')],
       default='singlelinetext',
       null=True))]
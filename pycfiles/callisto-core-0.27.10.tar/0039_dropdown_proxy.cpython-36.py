# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
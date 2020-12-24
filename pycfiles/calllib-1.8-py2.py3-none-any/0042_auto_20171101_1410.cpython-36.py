# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0042_auto_20171101_1410.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 646 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import callisto_core.wizard_builder.model_helpers

class Migration(migrations.Migration):
    dependencies = [
     ('wizard_builder', '0041_remove_formquestion_is_dropdown')]
    operations = [
     migrations.AlterField(model_name='choice',
       name='extra_info_text',
       field=models.TextField(blank=True, null=True)),
     migrations.AlterField(model_name='choice',
       name='text',
       field=models.TextField(null=True))]
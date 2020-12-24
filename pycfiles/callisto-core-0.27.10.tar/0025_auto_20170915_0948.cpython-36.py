# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0025_auto_20170915_0948.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 716 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('wizard_builder', '0024_remove_formquestion_added')]
    operations = [
     migrations.AlterField(model_name='formquestion',
       name='descriptive_text',
       field=models.TextField(blank=True)),
     migrations.AlterField(model_name='formquestion',
       name='text',
       field=models.TextField(blank=True)),
     migrations.AlterField(model_name='page',
       name='infobox',
       field=models.TextField(blank=True))]
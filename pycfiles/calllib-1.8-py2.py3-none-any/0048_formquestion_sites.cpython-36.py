# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0048_formquestion_sites.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 461 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('sites', '0002_alter_domain_unique'),
     ('wizard_builder', '0047_remove_formquestion_skip_eval')]
    operations = [
     migrations.AddField(model_name='formquestion',
       name='sites',
       field=models.ManyToManyField(to='sites.Site'))]
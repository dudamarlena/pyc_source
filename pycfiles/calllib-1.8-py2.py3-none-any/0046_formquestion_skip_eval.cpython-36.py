# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0046_formquestion_skip_eval.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 384 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('wizard_builder', '0045_auto_20171122_1808')]
    operations = [
     migrations.AddField(model_name='formquestion',
       name='skip_eval',
       field=models.BooleanField(default=True))]
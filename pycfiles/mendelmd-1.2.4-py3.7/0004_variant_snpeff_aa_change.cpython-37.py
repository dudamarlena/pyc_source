# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/variants/migrations/0004_variant_snpeff_aa_change.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 428 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('variants', '0003_variant_snpeff_codon_change')]
    operations = [
     migrations.AddField(model_name='variant',
       name='snpeff_aa_change',
       field=models.TextField(blank=True, db_index=True, null=True))]
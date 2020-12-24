# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0050_remove_page_sites.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 281 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('wizard_builder', '0049_copy_sites_from_page_to_question')]
    operations = [
     migrations.RemoveField(model_name='page', name='sites')]
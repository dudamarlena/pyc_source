# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0017_remove_unused_models.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 381 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('wizard_builder', '0016_checkboxes')]
    operations = [
     migrations.DeleteModel(name='Date'),
     migrations.DeleteModel(name='SingleLineTextWithMap')]
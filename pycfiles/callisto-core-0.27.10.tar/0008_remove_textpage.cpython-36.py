# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0008_remove_textpage.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 474 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('wizard_builder', '0007_remove_conditional')]
    operations = [
     migrations.RemoveField(model_name='textpage', name='pagebase_ptr'),
     migrations.AlterModelOptions(name='pagebase', options={}),
     migrations.DeleteModel(name='TextPage')]
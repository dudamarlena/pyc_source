# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0004_inheritence_downcasting.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 581 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('wizard_builder', '0003_multisite')]
    operations = [
     migrations.AlterModelManagers(name='questionpage', managers=[]),
     migrations.AlterModelManagers(name='textpage', managers=[]),
     migrations.RemoveField(model_name='formquestion', name='polymorphic_ctype'),
     migrations.RemoveField(model_name='pagebase', name='polymorphic_ctype')]
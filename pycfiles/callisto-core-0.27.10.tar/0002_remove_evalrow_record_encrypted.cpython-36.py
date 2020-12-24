# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/evaluation/migrations/0002_remove_evalrow_record_encrypted.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 273 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('evaluation', '0001_initial_eval_row')]
    operations = [
     migrations.RemoveField(model_name='evalrow', name='record_encrypted')]
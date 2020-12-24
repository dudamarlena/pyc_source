# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/theukdave/Documents/Code/DIT/dit-thumber/thumber/migrations/0002_rename_contentfeedback.py
# Compiled at: 2017-07-26 16:16:15
# Size of source mod 2**32: 702 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('thumber', '0001_initial')]
    operations = [
     migrations.RenameModel(old_name='ContentFeedback',
       new_name='Feedback'),
     migrations.AlterModelOptions(name='feedback',
       options={'ordering':('-created', ), 
      'verbose_name_plural':'Feedback'}),
     migrations.RenameField(model_name='feedback',
       old_name='utm_params',
       new_name='view_args')]
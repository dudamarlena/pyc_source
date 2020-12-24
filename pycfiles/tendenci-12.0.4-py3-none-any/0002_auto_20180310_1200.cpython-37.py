# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/emails/migrations/0002_auto_20180310_1200.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 349 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('emails', '0001_initial')]
    operations = [
     migrations.RenameField(model_name='Email',
       old_name='recipient_dispaly',
       new_name='recipient_display')]
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/user_groups/migrations/0002_group_show_for_memberships.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 545 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('user_groups', '0001_initial')]
    operations = [
     migrations.AddField(model_name='group',
       name='show_for_memberships',
       field=models.BooleanField(default=True, help_text='If checked and allows self add, this group will show as an option for the group field on membership applications'))]
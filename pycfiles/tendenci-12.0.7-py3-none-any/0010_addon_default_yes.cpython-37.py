# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/events/migrations/0010_addon_default_yes.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 534 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('events', '0009_sponsor_description')]
    operations = [
     migrations.AddField(model_name='addon',
       name='default_yes',
       field=models.BooleanField(default=False, help_text='Default the Add-on to yes so the registrant has to purposefully opt-out', verbose_name='Default to yes'))]
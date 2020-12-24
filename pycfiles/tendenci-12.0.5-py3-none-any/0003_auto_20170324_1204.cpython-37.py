# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/forms_builder/forms/migrations/0003_auto_20170324_1204.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 629 bytes
from django.db import migrations, models
import django.db.models.deletion, tendenci.apps.user_groups.utils

class Migration(migrations.Migration):
    dependencies = [
     ('user_groups', '0001_initial'),
     ('site_settings', '0001_initial'),
     ('search', '0001_initial'),
     ('forms', '0002_auto_20161208_2003')]
    operations = [
     migrations.AddField(model_name='form',
       name='group',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.SET_NULL), default=None, to='user_groups.Group', null=True))]
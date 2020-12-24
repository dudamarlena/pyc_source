# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/files/migrations/0005_auto_20180724_1745.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 561 bytes
from django.db import migrations, models
import django.db.models.deletion, tendenci.apps.user_groups.utils

class Migration(migrations.Migration):
    dependencies = [
     ('files', '0004_auto_20180315_0857')]
    operations = [
     migrations.AlterField(model_name='file',
       name='group',
       field=models.ForeignKey(default=None, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='user_groups.Group'))]
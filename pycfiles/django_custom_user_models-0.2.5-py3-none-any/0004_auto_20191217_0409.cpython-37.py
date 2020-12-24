# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\migrations\0004_auto_20191217_0409.py
# Compiled at: 2019-12-21 15:55:51
# Size of source mod 2**32: 598 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('CustomAuth', '0003_user_wallet')]
    operations = [
     migrations.RenameField(model_name='user',
       old_name='is_register',
       new_name='is_verify'),
     migrations.AlterField(model_name='user',
       name='last_name',
       field=models.CharField(blank=True, max_length=200, null=True, verbose_name='last name'))]
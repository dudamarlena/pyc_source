# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\migrations\0005_auto_20191218_1402.py
# Compiled at: 2019-12-21 15:55:51
# Size of source mod 2**32: 395 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('CustomAuth', '0004_auto_20191217_0409')]
    operations = [
     migrations.RenameField(model_name='user',
       old_name='permissions',
       new_name='user_permissions')]
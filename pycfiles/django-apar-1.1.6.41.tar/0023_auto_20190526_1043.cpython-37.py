# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0023_auto_20190526_1043.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 427 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0022_user_company_economical_number')]
    operations = [
     migrations.RenameField(model_name='devicelogin',
       old_name='device_type',
       new_name='device_type_temp')]
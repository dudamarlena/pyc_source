# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/breno/Envs/djangoplus/lib/python3.6/site-packages/djangoplus/admin/migrations/0009_auto_20170420_1238.py
# Compiled at: 2018-09-24 08:48:06
# Size of source mod 2**32: 705 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('admin', '0008_auto_20161124_1825')]
    operations = [
     migrations.RemoveField(model_name='settings',
       name='activated'),
     migrations.RemoveField(model_name='settings',
       name='admin_activation'),
     migrations.RemoveField(model_name='settings',
       name='associated_groups'),
     migrations.RemoveField(model_name='settings',
       name='mail_confirmation')]
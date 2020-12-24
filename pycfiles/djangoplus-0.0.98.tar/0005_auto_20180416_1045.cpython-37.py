# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/admin/migrations/0005_auto_20180416_1045.py
# Compiled at: 2018-10-05 12:53:01
# Size of source mod 2**32: 879 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('admin', '0004_auto_20180416_1037')]
    operations = [
     migrations.RemoveField(model_name='organizationrole',
       name='organization'),
     migrations.RemoveField(model_name='organizationrole',
       name='role'),
     migrations.RemoveField(model_name='unitrole',
       name='role'),
     migrations.RemoveField(model_name='unitrole',
       name='unit'),
     migrations.DeleteModel(name='OrganizationRole'),
     migrations.DeleteModel(name='UnitRole'),
     migrations.DeleteModel(name='Role')]
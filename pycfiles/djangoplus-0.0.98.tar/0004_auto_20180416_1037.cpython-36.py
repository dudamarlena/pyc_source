# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/breno/Envs/djangoplus/lib/python3.6/site-packages/djangoplus/admin/migrations/0004_auto_20180416_1037.py
# Compiled at: 2018-09-24 08:48:06
# Size of source mod 2**32: 1332 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    atomic = False
    dependencies = [
     ('admin', '0003_auto_20180416_1034')]
    operations = [
     migrations.RemoveField(model_name='organization',
       name='ascii'),
     migrations.RemoveField(model_name='unit',
       name='ascii'),
     migrations.RenameField(model_name='organization',
       old_name='id',
       new_name='scope_ptr'),
     migrations.RenameField(model_name='unit',
       old_name='id',
       new_name='scope_ptr'),
     migrations.AlterField(model_name='organization',
       name='scope_ptr',
       field=models.OneToOneField(auto_created=True, on_delete=(django.db.models.deletion.CASCADE), parent_link=True, primary_key=True, serialize=False, to='admin.Scope')),
     migrations.AlterField(model_name='unit',
       name='scope_ptr',
       field=models.OneToOneField(auto_created=True, on_delete=(django.db.models.deletion.CASCADE), parent_link=True, primary_key=True, serialize=False, to='admin.Scope'))]
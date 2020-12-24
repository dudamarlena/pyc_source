# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangocontact\src\djangocontact\migrations\0003_auto_20191014_1640.py
# Compiled at: 2019-10-14 07:10:59
# Size of source mod 2**32: 736 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('djangocontact', '0002_auto_20191014_1608')]
    operations = [
     migrations.RenameField(model_name='emailmodel',
       old_name='from_email',
       new_name='email'),
     migrations.RemoveField(model_name='emailmodel',
       name='phone_number'),
     migrations.RemoveField(model_name='emailmodel',
       name='subject'),
     migrations.RemoveField(model_name='emailmodel',
       name='to_email')]
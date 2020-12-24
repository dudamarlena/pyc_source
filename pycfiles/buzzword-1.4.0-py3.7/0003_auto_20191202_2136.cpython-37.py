# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/explore/migrations/0003_auto_20191202_2136.py
# Compiled at: 2020-05-05 16:46:09
# Size of source mod 2**32: 314 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('explore', '0002_auto_20191202_1431')]
    operations = [
     migrations.RenameField(model_name='corpus', old_name='len', new_name='length')]
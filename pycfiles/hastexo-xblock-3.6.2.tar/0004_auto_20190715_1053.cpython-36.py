# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/florian/git/hastexo-xblock/hastexo/migrations/0004_auto_20190715_1053.py
# Compiled at: 2020-03-13 09:19:09
# Size of source mod 2**32: 560 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('hastexo', '0003_blanks')]
    operations = [
     migrations.RemoveField(model_name='stacklog',
       name='stack'),
     migrations.AddField(model_name='stacklog',
       name='stack_id',
       field=models.IntegerField(db_index=True, null=True))]
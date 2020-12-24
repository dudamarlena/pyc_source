# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/um/migrations/0002_remove_umprofile_night_mode.py
# Compiled at: 2018-09-01 10:36:17
# Size of source mod 2**32: 319 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('um', '0001_initial')]
    operations = [
     migrations.RemoveField(model_name='umprofile',
       name='night_mode')]
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/Updoc/updoc/migrations/0002_uploaddoc_version.py
# Compiled at: 2017-07-28 01:43:32
# Size of source mod 2**32: 411 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('updoc', '0001_initial')]
    operations = [
     migrations.AddField(model_name='uploaddoc',
       name='version',
       field=models.IntegerField(blank=True, default=0, verbose_name='version'))]
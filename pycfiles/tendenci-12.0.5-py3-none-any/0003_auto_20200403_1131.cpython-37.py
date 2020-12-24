# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/photos/migrations/0003_auto_20200403_1131.py
# Compiled at: 2020-04-03 12:31:55
# Size of source mod 2**32: 437 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('photos', '0002_auto_20180315_0857')]
    operations = [
     migrations.AlterModelOptions(name='pool',
       options={'permissions':(('view_photopool', 'Can view photopool'), ), 
      'verbose_name':'pool',  'verbose_name_plural':'pools'})]
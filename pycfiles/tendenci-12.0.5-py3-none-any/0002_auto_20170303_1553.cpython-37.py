# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/staff/migrations/0002_auto_20170303_1553.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 362 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('staff', '0001_initial')]
    operations = [
     migrations.AddField(model_name='department',
       name='slug',
       field=models.SlugField(max_length=250, null=True))]
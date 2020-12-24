# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/profiles/migrations/0006_auto_20161025_1814.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 400 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('profiles', '0005_auto_20160330_1428')]
    operations = [
     migrations.AlterField(model_name='profile',
       name='direct_mail',
       field=models.BooleanField(default=True, verbose_name='direct mail'))]
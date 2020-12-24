# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/profiles/migrations/0009_auto_20180724_1308.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 474 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('profiles', '0008_auto_20180315_1839')]
    operations = [
     migrations.AlterField(model_name='profile',
       name='education',
       field=models.CharField(blank=True, max_length=100, verbose_name='highest level of education'))]
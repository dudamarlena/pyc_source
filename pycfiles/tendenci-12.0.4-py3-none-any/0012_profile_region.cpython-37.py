# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/profiles/migrations/0012_profile_region.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 460 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('profiles', '0011_auto_20190408_1603')]
    operations = [
     migrations.AddField(model_name='profile',
       name='region',
       field=models.CharField(blank=True, default='', max_length=50, verbose_name='region'))]
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/profiles/migrations/0011_auto_20190408_1603.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 666 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('profiles', '0010_auto_20181019_1640')]
    operations = [
     migrations.AddField(model_name='profile',
       name='is_billing_address',
       field=models.BooleanField(default=True, verbose_name='Is billing address')),
     migrations.AddField(model_name='profile',
       name='is_billing_address_2',
       field=models.BooleanField(default=False, verbose_name='Is billing address'))]
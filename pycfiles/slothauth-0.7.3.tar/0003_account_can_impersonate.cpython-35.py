# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/workspace/slothauth/test_mocks/migrations/0003_account_can_impersonate.py
# Compiled at: 2017-04-13 18:01:23
# Size of source mod 2**32: 608 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('test_mocks', '0002_auto_20160708_1811')]
    operations = [
     migrations.AddField(model_name='account', name='can_impersonate', field=models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='impersonate'))]
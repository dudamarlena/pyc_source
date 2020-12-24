# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/workspace/slothauth/test_mocks/migrations/0004_auto_20170816_1358.py
# Compiled at: 2017-08-16 16:58:29
# Size of source mod 2**32: 895 bytes
from __future__ import unicode_literals
from django.db import migrations
import slothauth.utils

class Migration(migrations.Migration):
    dependencies = [
     ('test_mocks', '0003_account_can_impersonate')]
    operations = [
     migrations.AlterField(model_name='account', name='one_time_authentication_key', field=slothauth.utils.RandomField(blank=True, max_length=32)),
     migrations.AlterField(model_name='account', name='password_reset_key', field=slothauth.utils.RandomField(blank=True, max_length=32)),
     migrations.AlterField(model_name='account', name='passwordless_key', field=slothauth.utils.RandomField(blank=True, max_length=32))]
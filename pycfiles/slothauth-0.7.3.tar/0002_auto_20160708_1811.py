# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/workspace/slothauth/test_mocks/migrations/0002_auto_20160708_1811.py
# Compiled at: 2016-07-08 21:11:39
from __future__ import unicode_literals
from django.db import migrations
import slothauth.utils

class Migration(migrations.Migration):
    dependencies = [
     ('test_mocks', '0001_initial')]
    operations = [
     migrations.AlterField(model_name=b'account', name=b'email', field=slothauth.utils.CiEmailField(max_length=254, unique=True, verbose_name=b'email address'))]
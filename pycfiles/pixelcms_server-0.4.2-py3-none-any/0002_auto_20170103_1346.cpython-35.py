# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-server/cms/accounts/migrations/0002_auto_20170103_1346.py
# Compiled at: 2017-01-03 07:46:46
# Size of source mod 2**32: 453 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('accounts', '0001_initial')]
    operations = [
     migrations.RemoveField(model_name='account', name='user'),
     migrations.DeleteModel(name='Account')]
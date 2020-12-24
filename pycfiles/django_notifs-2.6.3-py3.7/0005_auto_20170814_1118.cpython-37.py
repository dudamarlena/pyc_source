# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/notifications/migrations/0005_auto_20170814_1118.py
# Compiled at: 2019-02-21 19:34:58
# Size of source mod 2**32: 422 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('notifications', '0004_auto_20170719_1138')]
    operations = [
     migrations.AlterModelOptions(name='notification',
       options={'ordering': ('-id', )})]
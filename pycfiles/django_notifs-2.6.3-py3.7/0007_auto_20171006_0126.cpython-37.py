# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/notifications/migrations/0007_auto_20171006_0126.py
# Compiled at: 2019-02-21 19:34:58
# Size of source mod 2**32: 634 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('notifications', '0006_auto_20171005_0402')]
    operations = [
     migrations.AlterField(model_name='notification',
       name='obj',
       field=models.IntegerField(blank=True, null=True)),
     migrations.AlterField(model_name='notification',
       name='url',
       field=models.URLField(blank=True, null=True))]
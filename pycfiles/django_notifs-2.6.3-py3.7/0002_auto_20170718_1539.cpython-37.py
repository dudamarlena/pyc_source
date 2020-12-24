# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/notifications/migrations/0002_auto_20170718_1539.py
# Compiled at: 2019-02-21 19:34:58
# Size of source mod 2**32: 771 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('notifications', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='notification',
       name='source',
       field=models.ForeignKey(null=True, on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL))),
     migrations.AlterField(model_name='notification',
       name='source_display_name',
       field=models.CharField(max_length=150, null=True))]
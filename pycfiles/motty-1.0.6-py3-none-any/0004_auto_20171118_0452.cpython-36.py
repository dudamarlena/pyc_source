# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/idohyeon/Projects/motty/motty/app/migrations/0004_auto_20171118_0452.py
# Compiled at: 2017-11-17 23:52:19
# Size of source mod 2**32: 516 bytes
from __future__ import unicode_literals
import datetime
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('app', '0003_auto_20171118_0452')]
    operations = [
     migrations.AlterField(model_name='action',
       name='created_at',
       field=models.DateTimeField(default=(datetime.datetime(2017, 11, 18, 4, 52, 18, 606440))))]
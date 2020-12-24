# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/idohyeon/Projects/motty/motty/app/migrations/0005_auto_20171208_1314.py
# Compiled at: 2017-12-08 08:14:47
# Size of source mod 2**32: 847 bytes
from __future__ import unicode_literals
import datetime
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('app', '0004_auto_20171118_0452')]
    operations = [
     migrations.AlterField(model_name='action',
       name='created_at',
       field=models.DateTimeField(default=(datetime.datetime(2017, 12, 8, 13, 14, 47, 608551)))),
     migrations.AlterField(model_name='resource',
       name='name',
       field=models.CharField(max_length=30, unique=True)),
     migrations.AlterField(model_name='resource',
       name='url',
       field=models.CharField(max_length=50, unique=True))]
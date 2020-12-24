# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rowan/Nyaruka/dash/dash_test_runner/testapp/migrations/0002_auto_20180312_1302.py
# Compiled at: 2018-08-14 12:18:01
# Size of source mod 2**32: 346 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('testapp', '0001_initial')]
    operations = [
     migrations.AddField(model_name='contact',
       name='backend',
       field=models.CharField(default='rapidpro', max_length=16))]
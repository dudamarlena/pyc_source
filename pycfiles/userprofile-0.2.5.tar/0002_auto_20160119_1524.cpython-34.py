# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/aneumeier/github/userprofile/userprofile/migrations/0002_auto_20160119_1524.py
# Compiled at: 2016-01-19 10:24:01
# Size of source mod 2**32: 740 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('userprofile', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='profile', name='gender', field=models.CharField(choices=[('u', 'undefined'), ('M', 'Male'), ('F', 'Female')], default='u', max_length=1)),
     migrations.AlterField(model_name='profile', name='lookfor', field=models.CharField(choices=[('a', 'any'), ('M', 'Man'), ('F', 'Female')], default='a', max_length=1))]
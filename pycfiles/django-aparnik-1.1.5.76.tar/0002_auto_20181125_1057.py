# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/settings/migrations/0002_auto_20181125_1057.py
# Compiled at: 2018-11-25 03:12:47
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('settings', '0001_initial')]
    operations = [
     migrations.AddField(model_name=b'setting', name=b'is_variable_in_home', field=models.BooleanField(default=False, verbose_name=b'Is variable show in home')),
     migrations.AlterField(model_name=b'setting', name=b'value_type', field=models.CharField(choices=[('s', 'String'), ('i', 'Int'), ('b', 'Boolean'), ('dt', 'Date Time'), ('fr', 'Function setting return value')], max_length=31, verbose_name=b'Value Type'))]
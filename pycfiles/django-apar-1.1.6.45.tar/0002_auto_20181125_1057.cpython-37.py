# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/settings/migrations/0002_auto_20181125_1057.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 764 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('settings', '0001_initial')]
    operations = [
     migrations.AddField(model_name='setting',
       name='is_variable_in_home',
       field=models.BooleanField(default=False, verbose_name='Is variable show in home')),
     migrations.AlterField(model_name='setting',
       name='value_type',
       field=models.CharField(choices=[('s', 'String'), ('i', 'Int'), ('b', 'Boolean'), ('dt', 'Date Time'), ('fr', 'Function setting return value')], max_length=31, verbose_name='Value Type'))]
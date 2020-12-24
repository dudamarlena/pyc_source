# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0041_auto_20171030_1047.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 768 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0040_auto_20170926_2145')]
    operations = [
     migrations.AlterModelOptions(name='callbackentry',
       options={'verbose_name_plural':'Callback entries', 
      'verbose_name':'Callback entry'}),
     migrations.AlterModelOptions(name='companystatus',
       options={'verbose_name_plural': 'Company statuses'}),
     migrations.AlterModelOptions(name='opportunitypriority',
       options={'ordering':('name', ), 
      'verbose_name_plural':'opportunity priorities'})]
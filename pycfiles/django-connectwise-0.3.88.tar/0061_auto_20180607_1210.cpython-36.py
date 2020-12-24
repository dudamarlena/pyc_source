# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0061_auto_20180607_1210.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 1271 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0060_auto_20180605_0840')]
    operations = [
     migrations.AlterModelOptions(name='opportunitynote',
       options={'ordering':('-date_created', 'id'), 
      'verbose_name_plural':'Opportunity notes'}),
     migrations.AlterModelOptions(name='team',
       options={'ordering':('name', 'id'), 
      'verbose_name_plural':'Teams'}),
     migrations.AlterModelOptions(name='timeentry',
       options={'ordering':('-time_start', 'id'), 
      'verbose_name_plural':'Time entries'}),
     migrations.AddField(model_name='timeentry',
       name='detail_description_flag',
       field=models.BooleanField(default=False)),
     migrations.AddField(model_name='timeentry',
       name='internal_analysis_flag',
       field=models.BooleanField(default=False)),
     migrations.AddField(model_name='timeentry',
       name='resolution_flag',
       field=models.BooleanField(default=False))]
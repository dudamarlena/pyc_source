# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0084_auto_20190404_1532.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 1085 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0083_delete_callbackentry')]
    operations = [
     migrations.AlterField(model_name='servicenote',
       name='detail_description_flag',
       field=models.BooleanField(blank=True)),
     migrations.AlterField(model_name='servicenote',
       name='external_flag',
       field=models.BooleanField(blank=True)),
     migrations.AlterField(model_name='servicenote',
       name='internal_analysis_flag',
       field=models.BooleanField(blank=True)),
     migrations.AlterField(model_name='servicenote',
       name='internal_flag',
       field=models.BooleanField(blank=True)),
     migrations.AlterField(model_name='servicenote',
       name='resolution_flag',
       field=models.BooleanField(blank=True))]
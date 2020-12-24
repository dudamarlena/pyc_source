# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0062_auto_20180606_1117.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 1312 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0061_auto_20180605_1208')]
    operations = [
     migrations.CreateModel(name='Territory',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(blank=True, max_length=250, null=True))],
       options={'verbose_name_plural':'Territories', 
      'ordering':('name', )}),
     migrations.AlterModelOptions(name='opportunitynote',
       options={'ordering':('-date_created', 'id'), 
      'verbose_name_plural':'Opportunity notes'}),
     migrations.AlterModelOptions(name='timeentry',
       options={'ordering':('-time_start', 'id'), 
      'verbose_name_plural':'Time entries'}),
     migrations.AlterField(model_name='company',
       name='territory',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djconnectwise.Territory'))]
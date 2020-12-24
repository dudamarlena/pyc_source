# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0050_auto_20180417_1620.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 1000 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0049_auto_20180205_1122')]
    operations = [
     migrations.CreateModel(name='CompanyType',
       fields=[
      (
       'id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
      (
       'name', models.CharField(max_length=50)),
      (
       'vendor_flag', models.BooleanField())],
       options={'ordering': ('name', )}),
     migrations.RemoveField(model_name='company',
       name='type'),
     migrations.AddField(model_name='company',
       name='company_type',
       field=models.ForeignKey(blank=True, null=True, to='djconnectwise.CompanyType', on_delete=(models.SET_NULL)))]
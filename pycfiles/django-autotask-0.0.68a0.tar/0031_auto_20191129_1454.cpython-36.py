# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0031_auto_20191129_1454.py
# Compiled at: 2019-12-04 13:21:12
# Size of source mod 2**32: 1680 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0030_task_phase')]
    operations = [
     migrations.AlterModelOptions(name='account',
       options={'ordering': ('name', )}),
     migrations.AlterModelOptions(name='issuetype',
       options={'ordering': ('label', )}),
     migrations.AlterModelOptions(name='licensetype',
       options={'ordering': ('label', )}),
     migrations.AlterModelOptions(name='phase',
       options={'ordering': ('title', )}),
     migrations.AlterModelOptions(name='priority',
       options={'ordering':('sort_order', ), 
      'verbose_name_plural':'Priorities'}),
     migrations.AlterModelOptions(name='project',
       options={'ordering': ('name', )}),
     migrations.AlterModelOptions(name='projecttype',
       options={'ordering': ('label', )}),
     migrations.AlterModelOptions(name='source',
       options={'ordering': ('label', )}),
     migrations.AlterModelOptions(name='subissuetype',
       options={'ordering': ('label', )}),
     migrations.AlterModelOptions(name='ticketcategory',
       options={'ordering':('name', ), 
      'verbose_name_plural':'Ticket categories'}),
     migrations.AlterModelOptions(name='tickettype',
       options={'ordering': ('label', )})]
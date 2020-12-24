# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0037_auto_20170920_0959.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 829 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0036_auto_20170823_1417')]
    operations = [
     migrations.RenameField(model_name='opportunity',
       old_name='type',
       new_name='opportunity_type'),
     migrations.AlterField(model_name='opportunity',
       name='company',
       field=models.ForeignKey(to='djconnectwise.Company', related_name='company_opportunities', null=True, blank=True, on_delete=(models.SET_NULL))),
     migrations.AlterField(model_name='opportunity',
       name='expected_close_date',
       field=(models.DateTimeField()))]
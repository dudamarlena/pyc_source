# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0018_auto_20170505_1531.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 722 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0017_auto_20170504_2054')]
    operations = [
     migrations.AlterField(model_name='member',
       name='created',
       field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
     migrations.AlterField(model_name='member',
       name='modified',
       field=django_extensions.db.fields.ModificationDateTimeField(verbose_name='modified', auto_now=True))]
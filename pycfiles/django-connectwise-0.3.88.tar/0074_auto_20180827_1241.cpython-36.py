# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0074_auto_20180827_1241.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 697 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0073_auto_20180824_1446')]
    operations = [
     migrations.AlterField(model_name='slapriority',
       name='plan_within',
       field=(models.FloatField())),
     migrations.AlterField(model_name='slapriority',
       name='resolution_hours',
       field=(models.FloatField())),
     migrations.AlterField(model_name='slapriority',
       name='respond_hours',
       field=(models.FloatField()))]
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0059_auto_20180518_0811.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 502 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0058_auto_20180516_1052')]
    operations = [
     migrations.AlterField(model_name='callbackentry',
       name='member',
       field=models.ForeignKey(null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djconnectwise.Member'))]
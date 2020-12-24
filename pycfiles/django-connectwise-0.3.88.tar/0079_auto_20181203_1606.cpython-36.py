# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0079_auto_20181203_1606.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 1067 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0078_auto_20181203_1017')]
    operations = [
     migrations.AddField(model_name='ticket',
       name='type',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), related_name='type_tickets', to='djconnectwise.Type')),
     migrations.AlterField(model_name='ticket',
       name='sub_type',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), related_name='subtype_tickets', to='djconnectwise.SubType')),
     migrations.AlterField(model_name='ticket',
       name='sub_type_item',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), related_name='item_tickets', to='djconnectwise.Item'))]
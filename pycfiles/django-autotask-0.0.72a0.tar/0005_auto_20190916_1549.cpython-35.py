# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0005_auto_20190916_1549.py
# Compiled at: 2019-10-01 19:08:49
# Size of source mod 2**32: 1517 bytes
from django.db import migrations, models
import django.db.models.deletion, django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0004_auto_20190913_1425')]
    operations = [
     migrations.CreateModel(name='TicketSecondaryResource', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'resource', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.Resource')),
      (
       'ticket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.Ticket'))], options={'ordering': ('-modified', '-created'), 
      'get_latest_by': 'modified', 
      'abstract': False}),
     migrations.AddField(model_name='ticket', name='secondary_resources', field=models.ManyToManyField(related_name='secondary_resource_tickets', through='djautotask.TicketSecondaryResource', to='djautotask.Resource'))]
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0059_auto_20200414_1242.py
# Compiled at: 2020-04-16 20:47:33
# Size of source mod 2**32: 8223 bytes
from django.db import migrations, models
import django.db.models.deletion, django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0058_auto_20200408_1022')]
    operations = [
     migrations.CreateModel(name='ServiceCall',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'description', models.TextField(blank=True, max_length=2000, null=True)),
      (
       'duration', models.BigIntegerField(null=True)),
      (
       'complete', models.BooleanField(default=False)),
      (
       'create_date_time', models.DateTimeField(blank=True, null=True)),
      (
       'start_date_time', models.DateTimeField()),
      (
       'end_date_time', models.DateTimeField()),
      (
       'canceled_date_time', models.DateTimeField(blank=True, null=True)),
      (
       'last_modified_date_time', models.DateTimeField(blank=True, null=True)),
      (
       'account', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='djautotask.Account')),
      (
       'canceled_by_resource', models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djautotask.Resource')),
      (
       'creator_resource', models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djautotask.Resource'))],
       options={'ordering':('-modified', '-created'), 
      'get_latest_by':'modified', 
      'abstract':False}),
     migrations.CreateModel(name='ServiceCallStatus',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'label', models.CharField(blank=True, max_length=50, null=True)),
      (
       'is_default_value', models.BooleanField(default=False)),
      (
       'sort_order', models.PositiveSmallIntegerField(blank=True, null=True)),
      (
       'is_active', models.BooleanField(default=False)),
      (
       'is_system', models.BooleanField(default=False))],
       options={'ordering':('label', ), 
      'abstract':False}),
     migrations.CreateModel(name='ServiceCallTask',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'))],
       options={'ordering':('-modified', '-created'), 
      'get_latest_by':'modified', 
      'abstract':False}),
     migrations.CreateModel(name='ServiceCallTaskResource',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'resource', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='djautotask.Resource')),
      (
       'service_call_task', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='djautotask.ServiceCallTask'))],
       options={'ordering':('-modified', '-created'), 
      'get_latest_by':'modified', 
      'abstract':False}),
     migrations.CreateModel(name='ServiceCallTicket',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'))],
       options={'ordering':('-modified', '-created'), 
      'get_latest_by':'modified', 
      'abstract':False}),
     migrations.CreateModel(name='ServiceCallTicketResource',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'resource', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='djautotask.Resource')),
      (
       'service_call_ticket', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='djautotask.ServiceCallTicket'))],
       options={'ordering':('-modified', '-created'), 
      'get_latest_by':'modified', 
      'abstract':False}),
     migrations.AddField(model_name='servicecallticket',
       name='resources',
       field=models.ManyToManyField(related_name='resource_service_call_ticket', through='djautotask.ServiceCallTicketResource', to='djautotask.Resource')),
     migrations.AddField(model_name='servicecallticket',
       name='service_call',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='djautotask.ServiceCall')),
     migrations.AddField(model_name='servicecallticket',
       name='ticket',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='djautotask.Ticket')),
     migrations.AddField(model_name='servicecalltask',
       name='resources',
       field=models.ManyToManyField(related_name='resource_service_call_task', through='djautotask.ServiceCallTaskResource', to='djautotask.Resource')),
     migrations.AddField(model_name='servicecalltask',
       name='service_call',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='djautotask.ServiceCall')),
     migrations.AddField(model_name='servicecalltask',
       name='task',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='djautotask.Task')),
     migrations.AddField(model_name='servicecall',
       name='status',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='djautotask.ServiceCallStatus')),
     migrations.AddField(model_name='servicecall',
       name='tasks',
       field=models.ManyToManyField(related_name='task_service_calls', through='djautotask.ServiceCallTask', to='djautotask.Task')),
     migrations.AddField(model_name='servicecall',
       name='tickets',
       field=models.ManyToManyField(related_name='ticket_service_calls', through='djautotask.ServiceCallTicket', to='djautotask.Ticket'))]